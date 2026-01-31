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
    IncomeLevel,
    CityZone,
    PoliticalView,
)
from src.population import (
    generate_population,
    generate_initial_states,
    get_population_summary,
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
    if "states" not in st.session_state:
        st.session_state.states = None
    if "metrics" not in st.session_state:
        st.session_state.metrics = None
    if "population_config" not in st.session_state:
        st.session_state.population_config = None


def load_persisted_data() -> None:
    """
    Load persisted models and training data from disk.
    
    Reference: TECH_STACK.md Section 8 (Persistence Lifecycle)
    """
    # Models will be loaded when AI/ML is implemented
    pass


# =============================================================================
# UI Components
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
    import plotly.express as px
    import pandas as pd
    
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


def render_initial_metrics(metrics) -> None:
    """Render initial state metrics."""
    st.subheader("📊 Initial State Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Avg Happiness",
            format_percentage(metrics.avg_happiness),
        )
    with col2:
        st.metric(
            "Avg Policy Support",
            format_percentage(metrics.avg_support, include_sign=True),
        )
    with col3:
        st.metric(
            "Avg Income",
            format_currency(metrics.avg_income),
        )
    
    # Happiness by income level
    if metrics.happiness_by_income:
        st.markdown("**Happiness by Income Level**")
        cols = st.columns(len(metrics.happiness_by_income))
        for i, (level, happiness) in enumerate(metrics.happiness_by_income.items()):
            with cols[i]:
                st.metric(level.value, format_percentage(happiness))


def render_citizens_preview(citizens: list, states: list, max_rows: int = 10) -> None:
    """Render a preview table of citizens."""
    import pandas as pd
    
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
    if "happiness" in df.columns:
        df["happiness"] = df["happiness"].apply(lambda x: f"{x:.1%}")
    if "policy_support" in df.columns:
        df["policy_support"] = df["policy_support"].apply(lambda x: f"{x:+.1%}")
    if "income" in df.columns:
        df["income"] = df["income"].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)


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
        
        st.subheader("Population")
        population_size = st.slider(
            "Population Size",
            min_value=100,
            max_value=50_000,
            value=config.default_population_size,
            step=100,
            help="Number of synthetic citizens to generate",
        )
        
        # Income distribution sliders
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
            "Random Seed (optional)",
            min_value=0,
            max_value=999999,
            value=42,
            help="For reproducible population generation",
        )
        
        st.divider()
        
        # Generate button
        generate_disabled = high_pct < 0
        if st.button(
            "🎲 Generate Population",
            type="primary",
            disabled=generate_disabled,
            use_container_width=True,
        ):
            with st.spinner(f"Generating {population_size:,} citizens..."):
                try:
                    # Create config
                    pop_config = PopulationConfig(
                        size=population_size,
                        low_income_pct=low_pct,
                        middle_income_pct=middle_pct,
                        high_income_pct=high_pct,
                        random_seed=random_seed,
                    )
                    
                    # Generate population
                    rng = create_rng(random_seed)
                    population = generate_population(pop_config, rng)
                    states = generate_initial_states(population, rng)
                    metrics = calculate_step_metrics(population, states, step=0)
                    
                    # Store in session state
                    st.session_state.population = population
                    st.session_state.states = states
                    st.session_state.metrics = metrics
                    st.session_state.population_config = pop_config
                    
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
        
        st.subheader("Simulation")
        st.caption("Coming soon: Run simulations on generated populations")
        
        steps = st.slider(
            "Time Steps",
            min_value=1,
            max_value=10,
            value=config.default_simulation_steps,
            help="Number of simulation steps to run",
            disabled=True,
        )
        
        mode = st.selectbox(
            "Mode",
            options=["Precision", "Balanced", "Speed"],
            index=1,
            help="Precision: LLM only | Balanced: Hybrid | Speed: NN only",
            disabled=True,
        )
        
        st.button(
            "▶️ Run Simulation",
            type="secondary",
            disabled=True,
            use_container_width=True,
        )
    
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
    
    # Check if population has been generated
    if st.session_state.population is not None:
        # Display population data
        population = st.session_state.population
        states = st.session_state.states
        metrics = st.session_state.metrics
        
        # Summary statistics
        summary = get_population_summary(population)
        render_population_summary(summary)
        
        st.divider()
        
        # Distribution charts
        render_distribution_charts(summary)
        
        st.divider()
        
        # Initial metrics
        render_initial_metrics(metrics)
        
        st.divider()
        
        # Citizens preview
        render_citizens_preview(population, states)
        
    else:
        # Welcome state (no population generated yet)
        st.markdown("### 👋 Welcome to PolicyPulse")
        st.markdown(
            """
            Get started by generating a synthetic population:
            
            1. **Configure population size** in the sidebar (100 - 50,000 citizens)
            2. **Adjust income distribution** to match your scenario
            3. **Click "Generate Population"** to create your synthetic city
            
            Once generated, you'll see:
            - 📊 Population demographics and distributions
            - 📈 Initial happiness and income metrics
            - 👥 Preview of individual citizens
            """
        )
        
        with st.expander("💡 What is PolicyPulse?"):
            st.markdown(
                """
                PolicyPulse is an AI-powered tool that helps you understand how different 
                groups of people might react to policy changes.
                
                **Use cases:**
                - Test pricing changes before launching
                - Evaluate policy impact across demographics
                - Identify which groups may be most affected
                
                **How it works:**
                1. Generate a diverse synthetic population
                2. Define a policy to test
                3. Run a simulation to see reactions over time
                4. Analyze results by demographic groups
                """
            )
    
    # Configuration status
    st.divider()
    st.markdown("### 🔧 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if config.has_api_key:
            st.success("✅ Gemini API: Connected")
            logger.debug(f"API key configured: {config.mask_key(config.gemini_api_key)}")
        else:
            st.error("❌ Gemini API: Not configured")
            st.caption("Add GEMINI_API_KEY to .env file")
    
    with col2:
        if NN_MODEL_PATH.exists():
            st.success("✅ Neural Network: Trained")
        else:
            st.info("ℹ️ Neural Network: Not trained")
            st.caption("Run simulations in Precision/Balanced mode to collect training data")
    
    with col3:
        if st.session_state.population is not None:
            st.success(f"✅ Population: {len(st.session_state.population):,} citizens")
        else:
            st.info("ℹ️ Population: Not generated")
    
    # Debug info
    if config.debug:
        st.divider()
        with st.expander("🐛 Debug Information"):
            st.json({
                "project_root": str(PROJECT_ROOT),
                "debug_mode": config.debug,
                "api_key_configured": config.has_api_key,
                "backup_keys_count": len(config.gemini_backup_keys),
                "default_population": config.default_population_size,
                "default_steps": config.default_simulation_steps,
                "nn_min_samples": config.nn_min_training_samples,
                "population_generated": st.session_state.population is not None,
            })
    
    logger.debug("Application render complete")


if __name__ == "__main__":
    main()
