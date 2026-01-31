"""
PolicyPulse - Application Entry Point

Main Streamlit application with session management.
Reference: TECH_STACK.md Section 9 (Architecture Pattern)

This is the only module that should import from config.py.
Run with: streamlit run src/app.py
"""

from __future__ import annotations

import streamlit as st

# Page configuration must be first Streamlit command
st.set_page_config(
    page_title="PolicyPulse",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import (
    get_config,
    NN_MODEL_PATH,
    FEATURE_SCALER_PATH,
    TRAINING_DATA_PATH,
    PROJECT_ROOT,
)
from src.logging_config import setup_logging, get_logger
from src.data_models import (
    PopulationConfig,
    SimulationConfig,
    SimulationMode,
    Policy,
    PolicyDomain,
    IncomeLevel,
    CityZone,
    PoliticalView,
    SimulationResult,
)
from src.population import (
    generate_population,
    generate_initial_states,
    get_population_summary,
)
from src.simulation import (
    run_simulation,
    get_simulation_summary,
)
from src.stats import (
    calculate_step_metrics,
    create_citizens_dataframe,
)
from src.utils import (
    create_rng,
    format_currency,
    format_percentage,
)

# Initialize logging (once per session)
if "logger_initialized" not in st.session_state:
    config = get_config()
    setup_logging(debug=config.debug, log_file=config.log_file)
    st.session_state.logger_initialized = True

logger = get_logger("app")


# =============================================================================
# Session State Initialization
# =============================================================================

def init_session_state() -> None:
    """
    Initialize Streamlit session state with default values.
    
    Reference: TECH_STACK.md Section 8 (Session State for Runtime Data)
    """
    if "population" not in st.session_state:
        st.session_state.population = None
    if "initial_states" not in st.session_state:
        st.session_state.initial_states = None
    if "population_config" not in st.session_state:
        st.session_state.population_config = None
    if "simulation_result" not in st.session_state:
        st.session_state.simulation_result = None
    if "scenarios" not in st.session_state:
        st.session_state.scenarios = {}


def load_persisted_data() -> None:
    """
    Load persisted models and training data from disk.
    
    Reference: TECH_STACK.md Section 8 (Persistence Lifecycle)
    """
    # Models will be loaded when AI/ML is implemented
    pass


# =============================================================================
# UI Components - Population
# =============================================================================

def render_population_summary(summary: dict) -> None:
    """Render population summary statistics in a clean layout."""
    st.subheader("📊 Population Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Citizens", f"{summary['total']:,}")
    with col2:
        st.metric("Avg Age", f"{summary['avg_age']:.1f} years")
    with col3:
        st.metric("Avg Education", f"{summary['avg_education_years']:.1f} years")
    with col4:
        st.metric("Avg Family Size", f"{summary['avg_family_size']:.1f}")


def render_distribution_charts(summary: dict) -> None:
    """Render distribution charts for the population."""
    st.subheader("📈 Population Distributions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Income Level**")
        income_data = summary["income_distribution"]
        df = pd.DataFrame({
            "Level": list(income_data.keys()),
            "Count": list(income_data.values()),
        })
        fig = px.pie(df, values="Count", names="Level", hole=0.4)
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**City Zone**")
        zone_data = summary["zone_distribution"]
        df = pd.DataFrame({
            "Zone": list(zone_data.keys()),
            "Count": list(zone_data.values()),
        })
        fig = px.pie(df, values="Count", names="Zone", hole=0.4)
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("**Political View**")
        political_data = summary["political_distribution"]
        df = pd.DataFrame({
            "View": list(political_data.keys()),
            "Count": list(political_data.values()),
        })
        fig = px.pie(df, values="Count", names="View", hole=0.4)
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=250)
        st.plotly_chart(fig, use_container_width=True)


def render_citizens_preview(citizens: list, states: list, max_rows: int = 10) -> None:
    """Render a preview table of citizens."""
    st.subheader("👥 Citizen Preview")
    st.caption(f"Showing first {min(max_rows, len(citizens))} of {len(citizens):,} citizens")
    
    df = create_citizens_dataframe(citizens[:max_rows], states[:max_rows])
    
    # Select columns for display
    display_cols = [
        "id", "age", "gender", "income_level", "city_zone", 
        "profession", "happiness", "policy_support", "income"
    ]
    display_cols = [c for c in display_cols if c in df.columns]
    
    # Format numeric columns
    df_display = df.copy()
    if "happiness" in df_display.columns:
        df_display["happiness"] = df_display["happiness"].apply(lambda x: f"{x:.1%}")
    if "policy_support" in df_display.columns:
        df_display["policy_support"] = df_display["policy_support"].apply(lambda x: f"{x:+.1%}")
    if "income" in df_display.columns:
        df_display["income"] = df_display["income"].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_display[display_cols], use_container_width=True, hide_index=True)


# =============================================================================
# UI Components - Simulation Results
# =============================================================================

def render_simulation_metrics(result: SimulationResult) -> None:
    """Render simulation summary metrics with deltas."""
    summary = get_simulation_summary(result)
    
    st.subheader(f"📊 Simulation Results: {summary['scenario_name']}")
    st.caption(f"Policy: {summary['policy_title']} ({summary['policy_domain']}) | Steps: {summary['steps']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Final Happiness",
            format_percentage(summary["final_happiness"]),
            delta=format_percentage(summary["happiness_change"], include_sign=True),
        )
    
    with col2:
        st.metric(
            "Final Support",
            format_percentage(summary["final_support"], include_sign=True),
            delta=format_percentage(summary["support_change"], include_sign=True),
        )
    
    with col3:
        st.metric(
            "Final Avg Income",
            format_currency(summary["final_income"]),
            delta=format_currency(summary["income_change"]),
        )
    
    with col4:
        gap_delta = summary["gap_change"]
        gap_direction = "widened" if gap_delta > 0 else "narrowed"
        st.metric(
            "Happiness Gap",
            format_percentage(summary["final_gap"]),
            delta=f"{gap_direction} by {abs(gap_delta):.1%}",
            delta_color="inverse",  # Narrowing gap is good
        )


def render_time_series_charts(result: SimulationResult) -> None:
    """Render time-series charts for simulation metrics."""
    st.subheader("📈 Metrics Over Time")
    
    # Prepare data
    steps = [m.step for m in result.metrics_by_step]
    happiness = [m.avg_happiness for m in result.metrics_by_step]
    support = [m.avg_support for m in result.metrics_by_step]
    income = [m.avg_income for m in result.metrics_by_step]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Happiness over time
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=steps,
            y=[h * 100 for h in happiness],
            mode="lines+markers",
            name="Avg Happiness",
            line=dict(color="#667EEA", width=3),
            marker=dict(size=8),
        ))
        fig.update_layout(
            title="Happiness Over Time",
            xaxis_title="Simulation Step",
            yaxis_title="Happiness (%)",
            yaxis=dict(range=[0, 100]),
            margin=dict(t=40, b=40, l=40, r=20),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Support over time
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=steps,
            y=[s * 100 for s in support],
            mode="lines+markers",
            name="Avg Policy Support",
            line=dict(color="#764BA2", width=3),
            marker=dict(size=8),
        ))
        fig.update_layout(
            title="Policy Support Over Time",
            xaxis_title="Simulation Step",
            yaxis_title="Support (%)",
            yaxis=dict(range=[-100, 100]),
            margin=dict(t=40, b=40, l=40, r=20),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)


def render_demographic_breakdown(result: SimulationResult) -> None:
    """Render demographic breakdown charts."""
    st.subheader("👥 Impact by Demographic Group")
    
    # Get final metrics
    final_metrics = result.metrics_by_step[-1]
    initial_metrics = result.metrics_by_step[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Happiness by income level
        if final_metrics.happiness_by_income:
            levels = [level.value for level in IncomeLevel]
            initial_happiness = [initial_metrics.happiness_by_income.get(level, 0) * 100 for level in IncomeLevel]
            final_happiness = [final_metrics.happiness_by_income.get(level, 0) * 100 for level in IncomeLevel]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Initial",
                x=levels,
                y=initial_happiness,
                marker_color="#94a3b8",
            ))
            fig.add_trace(go.Bar(
                name="Final",
                x=levels,
                y=final_happiness,
                marker_color="#667EEA",
            ))
            fig.update_layout(
                title="Happiness by Income Level",
                xaxis_title="Income Level",
                yaxis_title="Happiness (%)",
                barmode="group",
                yaxis=dict(range=[0, 100]),
                margin=dict(t=40, b=40, l=40, r=20),
                height=300,
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Support by income level
        if final_metrics.support_by_income:
            levels = [level.value for level in IncomeLevel]
            initial_support = [initial_metrics.support_by_income.get(level, 0) * 100 for level in IncomeLevel]
            final_support = [final_metrics.support_by_income.get(level, 0) * 100 for level in IncomeLevel]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Initial",
                x=levels,
                y=initial_support,
                marker_color="#94a3b8",
            ))
            fig.add_trace(go.Bar(
                name="Final",
                x=levels,
                y=final_support,
                marker_color="#764BA2",
            ))
            fig.update_layout(
                title="Policy Support by Income Level",
                xaxis_title="Income Level",
                yaxis_title="Support (%)",
                barmode="group",
                yaxis=dict(range=[-100, 100]),
                margin=dict(t=40, b=40, l=40, r=20),
                height=300,
            )
            st.plotly_chart(fig, use_container_width=True)


def render_happiness_gap_evolution(result: SimulationResult) -> None:
    """Render happiness gap evolution chart."""
    st.subheader("📊 Inequality Evolution")
    
    steps = [m.step for m in result.metrics_by_step]
    gaps = [m.happiness_gap * 100 for m in result.metrics_by_step]
    
    # Create happiness by income level over time data
    data_rows = []
    for metrics in result.metrics_by_step:
        for level in IncomeLevel:
            happiness = metrics.happiness_by_income.get(level, 0)
            data_rows.append({
                "Step": metrics.step,
                "Income Level": level.value,
                "Happiness": happiness * 100,
            })
    
    df = pd.DataFrame(data_rows)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Happiness gap over time
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=steps,
            y=gaps,
            mode="lines+markers",
            fill="tozeroy",
            line=dict(color="#ef4444", width=2),
            marker=dict(size=6),
        ))
        fig.update_layout(
            title="Happiness Gap Over Time (High - Low Income)",
            xaxis_title="Simulation Step",
            yaxis_title="Gap (%)",
            margin=dict(t=40, b=40, l=40, r=20),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Happiness by income level over time
        fig = px.line(
            df,
            x="Step",
            y="Happiness",
            color="Income Level",
            markers=True,
            color_discrete_map={
                "Low": "#ef4444",
                "Middle": "#f59e0b",
                "High": "#22c55e",
            },
        )
        fig.update_layout(
            title="Happiness Trajectories by Income",
            xaxis_title="Simulation Step",
            yaxis_title="Happiness (%)",
            yaxis=dict(range=[0, 100]),
            margin=dict(t=40, b=40, l=40, r=20),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# Main Application
# =============================================================================

def main() -> None:
    """
    Main application entry point.
    
    Orchestrates the UI layout and user interactions.
    """
    logger.debug("Application starting")
    
    # Initialize
    init_session_state()
    load_persisted_data()
    
    # Load configuration
    config = get_config()
    
    # =========================================================================
    # Sidebar
    # =========================================================================
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # ---------------------------------------------------------------------
        # Population Configuration
        # ---------------------------------------------------------------------
        st.subheader("Population")
        population_size = st.slider(
            "Population Size",
            min_value=100,
            max_value=50_000,
            value=config.default_population_size,
            step=100,
            help="Number of synthetic citizens to generate",
        )
        
        with st.expander("Income Distribution", expanded=False):
            low_pct = st.slider(
                "Low Income %",
                min_value=0.0,
                max_value=1.0,
                value=0.30,
                step=0.05,
                format="%.0f%%",
            )
            middle_pct = st.slider(
                "Middle Income %",
                min_value=0.0,
                max_value=1.0,
                value=0.50,
                step=0.05,
                format="%.0f%%",
            )
            high_pct = 1.0 - low_pct - middle_pct
            st.info(f"High Income: {high_pct:.0%}")
            
            if high_pct < 0:
                st.error("Low + Middle cannot exceed 100%")
        
        random_seed = st.number_input(
            "Random Seed",
            min_value=0,
            max_value=999999,
            value=42,
            help="For reproducible generation",
        )
        
        # Generate Population Button
        generate_disabled = high_pct < 0
        if st.button(
            "🎲 Generate Population",
            type="primary",
            disabled=generate_disabled,
            use_container_width=True,
        ):
            with st.spinner(f"Generating {population_size:,} citizens..."):
                try:
                    pop_config = PopulationConfig(
                        size=population_size,
                        low_income_pct=low_pct,
                        middle_income_pct=middle_pct,
                        high_income_pct=high_pct,
                        random_seed=random_seed,
                    )
                    
                    rng = create_rng(random_seed)
                    population = generate_population(pop_config, rng)
                    initial_states = generate_initial_states(population, rng)
                    
                    st.session_state.population = population
                    st.session_state.initial_states = initial_states
                    st.session_state.population_config = pop_config
                    st.session_state.simulation_result = None  # Reset simulation
                    
                    logger.info(f"Generated population: {len(population)} citizens")
                    st.success(f"Generated {len(population):,} citizens!")
                    st.rerun()
                    
                except ValueError as e:
                    st.error(f"Configuration error: {e}")
                    logger.error(f"Population generation failed: {e}")
                except Exception as e:
                    st.error(f"Generation failed: {e}")
                    logger.exception("Population generation failed")
        
        st.divider()
        
        # ---------------------------------------------------------------------
        # Simulation Configuration
        # ---------------------------------------------------------------------
        st.subheader("Simulation")
        
        simulation_steps = st.slider(
            "Time Steps",
            min_value=1,
            max_value=10,
            value=config.default_simulation_steps,
            help="Number of simulation steps to run",
        )
        
        # Policy Configuration
        st.markdown("**Policy to Test**")
        policy_title = st.text_input(
            "Policy Title",
            value="New Economic Initiative",
            help="Name of the policy being tested",
        )
        
        policy_domain = st.selectbox(
            "Policy Domain",
            options=[d.value for d in PolicyDomain],
            index=0,
            help="Category of the policy",
        )
        
        policy_description = st.text_area(
            "Description",
            value="A comprehensive policy aimed at stimulating economic growth.",
            height=80,
            help="Brief description of the policy",
        )
        
        # Run Simulation Button
        sim_disabled = st.session_state.population is None
        if st.button(
            "▶️ Run Simulation",
            type="primary",
            disabled=sim_disabled,
            use_container_width=True,
        ):
            if st.session_state.population is None:
                st.error("Please generate a population first")
            else:
                with st.spinner(f"Running simulation ({simulation_steps} steps)..."):
                    try:
                        # Create policy
                        policy = Policy(
                            title=policy_title,
                            description=policy_description,
                            domain=PolicyDomain(policy_domain),
                        )
                        
                        # Create simulation config
                        sim_config = SimulationConfig(
                            mode=SimulationMode.SPEED,  # Rule-based for now
                            steps=simulation_steps,
                        )
                        
                        # Generate scenario name
                        scenario_name = f"{policy_title[:30]} - Step {len(st.session_state.scenarios) + 1}"
                        
                        # Create fresh RNG for simulation
                        pop_config = st.session_state.population_config
                        rng = create_rng(pop_config.random_seed)
                        
                        # Run simulation
                        result = run_simulation(
                            policy=policy,
                            citizens=st.session_state.population,
                            initial_states=st.session_state.initial_states,
                            config=sim_config,
                            population_config=pop_config,
                            scenario_name=scenario_name,
                            rng=rng,
                        )
                        
                        # Store result
                        st.session_state.simulation_result = result
                        st.session_state.scenarios[scenario_name] = result
                        
                        logger.info(f"Simulation complete: {scenario_name}")
                        st.success("Simulation complete!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Simulation failed: {e}")
                        logger.exception("Simulation failed")
        
        if sim_disabled:
            st.caption("⚠️ Generate a population first")
        
        st.divider()
        
        # ---------------------------------------------------------------------
        # System Status
        # ---------------------------------------------------------------------
        st.subheader("Status")
        
        if st.session_state.population:
            st.success(f"✅ {len(st.session_state.population):,} citizens")
        else:
            st.info("ℹ️ No population")
        
        if st.session_state.simulation_result:
            st.success("✅ Simulation run")
        else:
            st.info("ℹ️ No simulation")
    
    # =========================================================================
    # Main Content
    # =========================================================================
    
    # Header
    st.markdown(
        """
        <h1 style="background: linear-gradient(90deg, #667EEA 0%, #764BA2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 2.5rem; margin-bottom: 0;">
            🎯 PolicyPulse
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.caption("AI-powered synthetic population simulator for stress-testing policies")
    
    # Disclaimer
    st.warning(
        "⚠️ **Synthetic Simulation Disclaimer**: This tool creates fictional scenarios "
        "for exploratory purposes. Results do not predict real-world behavior. "
        "Use as a thought experiment to identify potential blind spots—not as a "
        "substitute for real data, surveys, or expert analysis."
    )
    
    st.divider()
    
    # =========================================================================
    # Content based on state
    # =========================================================================
    
    # Show simulation results if available
    if st.session_state.simulation_result is not None:
        result = st.session_state.simulation_result
        
        # Summary metrics
        render_simulation_metrics(result)
        
        st.divider()
        
        # Time series charts
        render_time_series_charts(result)
        
        st.divider()
        
        # Demographic breakdown
        render_demographic_breakdown(result)
        
        st.divider()
        
        # Inequality evolution
        render_happiness_gap_evolution(result)
        
        st.divider()
        
        # Population context
        with st.expander("📋 Population Details", expanded=False):
            summary = get_population_summary(result.citizens)
            render_population_summary(summary)
            render_distribution_charts(summary)
            
            # Final state preview
            final_states = result.states_by_step[result.config.steps]
            render_citizens_preview(result.citizens, final_states)
    
    elif st.session_state.population is not None:
        # Population generated but no simulation yet
        population = st.session_state.population
        initial_states = st.session_state.initial_states
        
        st.info("👆 Configure a policy in the sidebar and click **Run Simulation** to see results")
        
        st.divider()
        
        # Show population info
        summary = get_population_summary(population)
        render_population_summary(summary)
        
        st.divider()
        
        render_distribution_charts(summary)
        
        st.divider()
        
        # Initial metrics
        initial_metrics = calculate_step_metrics(population, initial_states, step=0)
        st.subheader("📊 Initial State Metrics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Happiness", format_percentage(initial_metrics.avg_happiness))
        with col2:
            st.metric("Avg Support", format_percentage(initial_metrics.avg_support, include_sign=True))
        with col3:
            st.metric("Avg Income", format_currency(initial_metrics.avg_income))
        
        st.divider()
        
        render_citizens_preview(population, initial_states)
        
    else:
        # Welcome state
        st.markdown("### 👋 Welcome to PolicyPulse")
        st.markdown(
            """
            Get started in two steps:
            
            1. **Generate a population** in the sidebar (100 - 50,000 citizens)
            2. **Configure and run a simulation** to see how policies affect different groups
            
            After running a simulation, you'll see:
            - 📊 Summary metrics with changes from initial state
            - 📈 Time-series charts showing evolution over steps
            - 👥 Demographic breakdowns by income level
            - 📉 Inequality gap tracking
            """
        )
        
        with st.expander("💡 Understanding Policy Domains"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🏦 Economy**")
                st.markdown("Tax cuts, interest rates, trade policies. Often favor higher income groups.")
                
                st.markdown("**📚 Education**")
                st.markdown("School funding, training programs. Typically help lower income groups most.")
            
            with col2:
                st.markdown("**🤝 Social**")
                st.markdown("Healthcare, housing, welfare. Strong impact on vulnerable populations.")
                
                st.markdown("**💼 Business**")
                st.markdown("Deregulation, incentives, subsidies. Usually benefit business owners.")
    
    # Debug info
    if config.debug:
        st.divider()
        with st.expander("🐛 Debug Information"):
            st.json({
                "project_root": str(PROJECT_ROOT),
                "debug_mode": config.debug,
                "population_generated": st.session_state.population is not None,
                "population_size": len(st.session_state.population) if st.session_state.population else 0,
                "simulation_run": st.session_state.simulation_result is not None,
                "scenarios_count": len(st.session_state.scenarios),
            })
    
    logger.debug("Application render complete")


if __name__ == "__main__":
    main()
