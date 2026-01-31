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
    ReactionMethod,
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
from src.llm_client import (
    create_llm_client,
    LLMClient,
    LLMNotConfiguredError,
)

# =============================================================================
# Premium Modern UI with 3D Effects & Sophisticated Animations
# =============================================================================

def inject_custom_css():
    """Inject premium custom CSS with sophisticated hover effects, 3D transforms, and GPU-accelerated animations."""
    st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Accessibility: Reduced Motion Support */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* Root Variables for Premium Theme */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
        --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.16);
        --shadow-xl: 0 20px 48px rgba(0, 0, 0, 0.24);
        --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-smooth: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        --blur-glass: blur(12px);
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Global Enhancements */
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Main Container with Glass Effect */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1400px;
    }
    
    /* Premium Gradient Headers with 3D Effects */
    .gradient-header {
        position: relative;
        background: var(--primary-gradient);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: var(--shadow-lg);
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
        will-change: transform;
        transition: all var(--transition-smooth);
    }
    
    @media (min-width: 768px) {
        .gradient-header:hover {
            transform: translateY(-8px) rotateX(2deg);
            box-shadow: var(--shadow-xl), 0 0 60px rgba(102, 126, 234, 0.4);
        }
        
        .gradient-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity var(--transition-smooth);
            pointer-events: none;
        }
        
        .gradient-header:hover::before {
            opacity: 1;
            animation: shimmer 2s ease-in-out infinite;
        }
    }
    
    @keyframes shimmer {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(10%, 10%) rotate(5deg); }
    }
    
    .section-header {
        background: var(--primary-gradient);
        padding: 20px 30px;
        border-radius: 16px;
        color: white;
        margin: 30px 0 20px 0;
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
        transform: translateZ(0);
        will-change: transform;
        transition: all var(--transition-base);
    }
    
    @media (min-width: 768px) {
        .section-header:hover {
            transform: translateX(8px) scale(1.02);
            box-shadow: var(--shadow-lg);
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2));
            transform: translateX(-100%);
            transition: transform var(--transition-smooth);
        }
        
        .section-header:hover::after {
            transform: translateX(400%);
        }
    }
    
    /* Ultra-Premium Metric Cards with 3D Lift */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
        will-change: transform, box-shadow;
        transition: all var(--transition-smooth);
        backdrop-filter: var(--blur-glass);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--primary-gradient);
        opacity: 0;
        transition: opacity var(--transition-base);
        z-index: -1;
    }
    
    @media (min-width: 768px) {
        .metric-card:hover {
            transform: translateY(-12px) scale(1.03) rotateX(5deg);
            box-shadow: var(--shadow-xl), 0 0 40px rgba(102, 126, 234, 0.3);
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .metric-card:hover::before {
            opacity: 0.03;
        }
        
        .metric-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 4px;
            background: var(--primary-gradient);
            transition: width var(--transition-smooth) 0.1s;
        }
        
        .metric-card:hover::after {
            width: 100%;
        }
    }
    
    /* Animated Status Badges with Glow */
    .badge {
        padding: 8px 18px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin: 5px;
        position: relative;
        overflow: hidden;
        transform: translateZ(0);
        will-change: transform, box-shadow;
        transition: all var(--transition-base);
        cursor: default;
    }
    
    @media (min-width: 768px) {
        .badge:hover {
            transform: scale(1.1) translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }
    }
    
    .badge-success { 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
        color: white; 
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .badge-warning { 
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
        color: white; 
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    .badge-info { 
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
        color: white; 
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .badge-danger { 
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
        color: white; 
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    @media (min-width: 768px) {
        .badge-success:hover { box-shadow: 0 8px 24px rgba(16, 185, 129, 0.5); }
        .badge-warning:hover { box-shadow: 0 8px 24px rgba(245, 158, 11, 0.5); }
        .badge-info:hover { box-shadow: 0 8px 24px rgba(59, 130, 246, 0.5); }
        .badge-danger:hover { box-shadow: 0 8px 24px rgba(239, 68, 68, 0.5); }
    }
    
    /* Premium Button Transformations */
    .stButton > button {
        border-radius: 14px;
        font-weight: 600;
        padding: 12px 32px;
        background: var(--primary-gradient);
        color: white;
        border: none;
        position: relative;
        overflow: hidden;
        transform: translateZ(0);
        will-change: transform, box-shadow;
        transition: all var(--transition-base);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width var(--transition-smooth), height var(--transition-smooth);
    }
    
    @media (min-width: 768px) {
        .stButton > button:hover {
            transform: translateY(-4px) scale(1.05);
            box-shadow: var(--shadow-lg), 0 0 30px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:active {
            transform: translateY(-2px) scale(1.02);
        }
    }
    
    /* Enhanced Metrics with Stagger Animation */
    [data-testid="stMetricValue"] {
        font-size: 2.4rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: metricFadeIn 0.6s ease-out;
    }
    
    @keyframes metricFadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.85rem;
    }
    
    /* Premium Tabs with Morphing Effect */
    .stTabs {
        background: white;
        border-radius: 16px;
        padding: 8px;
        box-shadow: var(--shadow-sm);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all var(--transition-base);
        position: relative;
        overflow: hidden;
    }
    
    @media (min-width: 768px) {
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(102, 126, 234, 0.1);
            transform: scale(1.05);
        }
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
        box-shadow: var(--shadow-md);
        transform: scale(1.05);
    }
    
    /* Premium Charts with Glow Effect */
    .js-plotly-plot {
        border-radius: 16px;
        box-shadow: var(--shadow-md);
        background: white;
        padding: 10px;
        transition: all var(--transition-base);
        transform: translateZ(0);
        will-change: transform, box-shadow;
    }
    
    @media (min-width: 768px) {
        .js-plotly-plot:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }
    }
    
    /* Sidebar Premium Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        box-shadow: var(--shadow-lg);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Input Fields Enhancement */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px;
        transition: all var(--transition-base);
    }
    
    @media (min-width: 768px) {
        .stTextInput input:hover, .stTextArea textarea:hover, .stSelectbox select:hover {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: scale(1.01);
        }
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        transform: scale(1.01);
    }
    
    /* Expander Premium Style */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        font-weight: 600;
        padding: 16px;
        transition: all var(--transition-base);
    }
    
    @media (min-width: 768px) {
        .streamlit-expanderHeader:hover {
            background: var(--primary-gradient);
            color: white;
            transform: translateX(8px);
            box-shadow: var(--shadow-md);
        }
    }
    
    /* Progress Bar Enhancement */
    .stProgress > div > div {
        background: var(--primary-gradient);
        border-radius: 10px;
        height: 12px;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
        animation: spin 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Alert/Info Boxes */
    .stAlert {
        border-radius: 14px;
        border-left: 5px solid;
        padding: 20px;
        backdrop-filter: var(--blur-glass);
        transition: all var(--transition-base);
    }
    
    @media (min-width: 768px) {
        .stAlert:hover {
            transform: translateX(8px);
            box-shadow: var(--shadow-md);
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
        transition: all var(--transition-base);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Keyboard Focus Indicators for Accessibility */
    button:focus-visible, 
    input:focus-visible, 
    select:focus-visible, 
    textarea:focus-visible {
        outline: 3px solid #667eea;
        outline-offset: 2px;
    }
    
    /* Staggered Animation for Multiple Elements */
    @media (min-width: 768px) {
        .metric-card:nth-child(1) { animation-delay: 0s; }
        .metric-card:nth-child(2) { animation-delay: 0.1s; }
        .metric-card:nth-child(3) { animation-delay: 0.2s; }
        .metric-card:nth-child(4) { animation-delay: 0.3s; }
    }
    
    /* Success/Error Messages with Slide-in Animation */
    .stSuccess, .stError, .stWarning, .stInfo {
        animation: slideIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border-radius: 14px;
        padding: 18px;
        box-shadow: var(--shadow-md);
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Mobile Optimization */
    @media (max-width: 767px) {
        .gradient-header {
            padding: 25px 15px;
            margin-bottom: 20px;
        }
        
        .metric-card {
            padding: 20px;
            margin: 15px 0;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

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
    if "llm_client" not in st.session_state:
        st.session_state.llm_client = None
    if "ai_enabled" not in st.session_state:
        st.session_state.ai_enabled = False


def init_llm_client() -> LLMClient | None:
    """
    Initialize LLM client if API keys are configured.
    
    Returns the client or None if not configured.
    """
    if st.session_state.llm_client is not None:
        return st.session_state.llm_client
    
    config = get_config()
    if config.has_api_key:
        try:
            client = create_llm_client(config.all_api_keys)
            st.session_state.llm_client = client
            logger.info("LLM client initialized successfully")
            return client
        except LLMNotConfiguredError:
            logger.info("LLM client not configured (no valid API keys)")
            return None
    return None


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
        st.plotly_chart(fig, key="income_distribution_pie", width='stretch')
    
    with col2:
        st.markdown("**City Zone**")
        zone_data = summary["zone_distribution"]
        df = pd.DataFrame({
            "Zone": list(zone_data.keys()),
            "Count": list(zone_data.values()),
        })
        fig = px.pie(df, values="Count", names="Zone", hole=0.4)
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=250)
        st.plotly_chart(fig, key="zone_distribution_pie", width='stretch')
    
    with col3:
        st.markdown("**Political View**")
        political_data = summary["political_distribution"]
        df = pd.DataFrame({
            "View": list(political_data.keys()),
            "Count": list(political_data.values()),
        })
        fig = px.pie(df, values="Count", names="View", hole=0.4)
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=250)
        st.plotly_chart(fig, key="political_distribution_pie", width='stretch')


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
    
    st.dataframe(df_display[display_cols], width='stretch', hide_index=True)


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


def render_time_series_charts(result: SimulationResult, key_prefix: str = "") -> None:
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
        st.plotly_chart(fig, key=f"{key_prefix}happiness_over_time", width='stretch')
    
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
        st.plotly_chart(fig, key=f"{key_prefix}support_over_time", width='stretch')


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
            st.plotly_chart(fig, key="happiness_by_income", width='stretch')
    
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
            st.plotly_chart(fig, key="support_by_income", width='stretch')


def render_happiness_gap_evolution(result: SimulationResult, key_prefix: str = "") -> None:
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
        st.plotly_chart(fig, key=f"{key_prefix}happiness_gap_over_time", width='stretch')
    
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
        st.plotly_chart(fig, key=f"{key_prefix}happiness_trajectories", width='stretch')


def render_ai_status(result: SimulationResult) -> None:
    """Render AI integration status and insights."""
    ai_status = result.ai_status
    
    st.subheader("🤖 AI & Processing Status")
    
    if ai_status is None:
        # No AI status - show rule-based information
        st.info("🎯 **Rule-Based Simulation Mode**\n\nThis simulation used deterministic rule-based logic to model citizen reactions. This mode is fast, reliable, and doesn't require API keys.")
        
        # Show method breakdown from method_counts
        if result.method_counts:
            st.markdown("---")
            st.markdown("**📊 Processing Method Breakdown**")
            
            # Aggregate across all steps
            total_rule = sum(
                counts.get(ReactionMethod.RULE_BASED, 0)
                for counts in result.method_counts.values()
            )
            total_neural = sum(
                counts.get(ReactionMethod.NEURAL_NETWORK, 0)
                for counts in result.method_counts.values()
            )
            total_llm = sum(
                counts.get(ReactionMethod.LLM, 0)
                for counts in result.method_counts.values()
            )
            total = total_rule + total_neural + total_llm
            
            if total > 0:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    rule_pct = (total_rule / total) * 100
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: center;">
                        <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                            ⚙️ Rule-Based
                        </div>
                        <div style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;">
                            {rule_pct:.1f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(rule_pct / 100)
                
                with col2:
                    if total_neural > 0:
                        neural_pct = (total_neural / total) * 100
                        st.markdown(f"""
                        <div class="metric-card" style="text-align: center;">
                            <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                                🧠 Neural Network
                            </div>
                            <div style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;">
                                {neural_pct:.1f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.progress(neural_pct / 100)
                    else:
                        st.markdown("""
                        <div class="metric-card" style="text-align: center; opacity: 0.5;">
                            <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                                🧠 Neural Network
                            </div>
                            <div style="font-size: 2.8rem; font-weight: 800; color: #cbd5e1; margin-bottom: 12px;">
                                0%
                            </div>
                            <div style="color: #cbd5e1; font-size: 0.85rem;">
                                Not used
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col3:
                    if total_llm > 0:
                        llm_pct = (total_llm / total) * 100
                        st.metric("AI/LLM", f"{llm_pct:.1f}%")
                        st.progress(llm_pct / 100)
                    else:
                        st.metric("AI/LLM", "0%")
                        st.caption("LLM not used")
                
                # Additional stats
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Simulation Reliability**")
                    st.success("100% deterministic - all reactions computed locally")
                    st.caption(f"Total reactions: {total:,}")
                
                with col2:
                    st.markdown("**⚡ Performance**")
                    st.success("Fast execution - no API latency")
                    st.caption(f"Population: {len(result.citizens):,} citizens")
        
        return
    
    if not ai_status.ai_enabled:
        st.info("AI enhancement was not enabled for this simulation. Results are fully rule-based.")
        
        # Show method breakdown even when AI not enabled
        if result.method_counts:
            st.markdown("---")
            st.markdown("**📊 Processing Method Breakdown**")
            
            total_rule = sum(
                counts.get(ReactionMethod.RULE_BASED, 0)
                for counts in result.method_counts.values()
            )
            total_neural = sum(
                counts.get(ReactionMethod.NEURAL_NETWORK, 0)
                for counts in result.method_counts.values()
            )
            total = total_rule + total_neural
            
            if total > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    rule_pct = (total_rule / total) * 100
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: center;">
                        <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                            ⚙️ Rule-Based
                        </div>
                        <div style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;">
                            {rule_pct:.1f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(rule_pct / 100)
                
                with col2:
                    if total_neural > 0:
                        neural_pct = (total_neural / total) * 100
                        st.markdown(f"""
                        <div class="metric-card" style="text-align: center;">
                            <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                                🧠 Neural Network
                            </div>
                            <div style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;">
                                {neural_pct:.1f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.progress(neural_pct / 100)
                    else:
                        st.markdown("""
                        <div class="metric-card" style="text-align: center; opacity: 0.5;">
                            <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                                🧠 Neural Network
                            </div>
                            <div style="font-size: 2.8rem; font-weight: 800; color: #cbd5e1; margin-bottom: 12px;">
                                0%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        return
    
    # AI was enabled - show full status
    st.markdown('<div class="metric-card" style="border-left-color: #667eea;">', unsafe_allow_html=True)
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if ai_status.ai_available:
            st.metric("AI Status", "✅ Active", delta=None)
        else:
            st.metric("AI Status", "⚠️ Unavailable", delta=None)
    
    with col2:
        st.metric("Citizens Sampled", f"{ai_status.citizens_sampled:,}")
    
    with col3:
        st.metric("AI Successes", f"{ai_status.ai_successes:,}")
    
    with col4:
        fallback_rate = (
            (ai_status.ai_failures / max(1, ai_status.citizens_sampled)) * 100
            if ai_status.citizens_sampled > 0 else 0
        )
        st.metric(
            "Fallback Rate",
            f"{fallback_rate:.1f}%",
            delta="lower is better" if fallback_rate < 10 else "some fallbacks",
            delta_color="off",
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show AI insight if available
    if result.ai_insight:
        st.markdown("---")
        st.markdown("**🔍 AI-Generated Insight**")
        st.markdown(
            f'<div style="background-color: #f0f4ff; padding: 15px; border-radius: 8px; '
            f'border-left: 4px solid #667EEA;">'
            f'<em>{result.ai_insight}</em>'
            f'<br><small style="color: #666;">⚡ Generated by AI - for exploratory purposes only</small>'
            f'</div>',
            unsafe_allow_html=True,
        )
    
    # Show errors if any
    if ai_status.error_message:
        with st.expander("⚠️ AI Errors Encountered", expanded=False):
            st.warning(
                f"Some AI requests failed and used rule-based fallback:\n\n"
                f"`{ai_status.error_message}`"
            )
    
    # Method breakdown
    if result.method_counts:
        st.markdown("---")
        st.markdown("**📊 Processing Method Breakdown**")
        
        # Aggregate across all steps
        total_rule = sum(
            counts.get(ReactionMethod.RULE_BASED, 0)
            for counts in result.method_counts.values()
        )
        total_neural = sum(
            counts.get(ReactionMethod.NEURAL_NETWORK, 0)
            for counts in result.method_counts.values()
        )
        total_llm = sum(
            counts.get(ReactionMethod.LLM, 0)
            for counts in result.method_counts.values()
        )
        total = total_rule + total_neural + total_llm
        
        if total > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rule_pct = (total_rule / total) * 100
                st.markdown(f"""
                <div class="metric-card" style="text-align: center;">
                    <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                        ⚙️ Rule-Based
                    </div>
                    <div style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;">
                        {rule_pct:.1f}%
                    </div>
                    <div style="color: #94a3b8; font-size: 0.95rem; font-weight: 500;">
                        {total_rule:,} reactions
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(rule_pct / 100)
            
            with col2:
                if total_neural > 0:
                    neural_pct = (total_neural / total) * 100
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: center;">
                        <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                            🧠 Neural Network
                        </div>
                        <div style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;">
                            {neural_pct:.1f}%
                        </div>
                        <div style="color: #94a3b8; font-size: 0.95rem; font-weight: 500;">
                            {total_neural:,} reactions
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(neural_pct / 100)
                else:
                    st.markdown("""
                    <div class="metric-card" style="text-align: center; opacity: 0.5;">
                        <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                            🧠 Neural Network
                        </div>
                        <div style="font-size: 2.8rem; font-weight: 800; color: #cbd5e1; margin-bottom: 12px;">
                            0%
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.85rem;">
                            Not used
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                if total_llm > 0:
                    llm_pct = (total_llm / total) * 100
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: center;">
                        <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                            ✨ AI/LLM
                        </div>
                        <div style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px;">
                            {llm_pct:.1f}%
                        </div>
                        <div style="color: #94a3b8; font-size: 0.95rem; font-weight: 500;">
                            {total_llm:,} reactions
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(llm_pct / 100)
                else:
                    st.markdown("""
                    <div class="metric-card" style="text-align: center; opacity: 0.5;">
                        <div style="color: #64748b; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                            ✨ AI/LLM
                        </div>
                        <div style="font-size: 2.8rem; font-weight: 800; color: #cbd5e1; margin-bottom: 12px;">
                            0%
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.85rem;">
                            Not used
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


def render_sample_explanations(result: SimulationResult, max_samples: int = 5) -> None:
    """Render sample citizen explanations from AI or rules."""
    if not result.config.ai_explanation_enabled:
        return
    
    # Get final states with explanations
    final_step = result.config.steps
    final_states = result.states_by_step.get(final_step, [])
    states_with_explanations = [
        s for s in final_states
        if s.diary_entry is not None and s.diary_entry.strip()
    ]
    
    if not states_with_explanations:
        return
    
    st.subheader("💭 Sample Citizen Perspectives")
    st.caption("Short explanations of how individual citizens reacted to the policy")
    
    # Get citizen lookup
    citizen_by_id = {c.id: c for c in result.citizens}
    
    # Show sample
    for state in states_with_explanations[:max_samples]:
        citizen = citizen_by_id.get(state.citizen_id)
        if not citizen:
            continue
        
        method_badge = "🤖 AI" if state.reaction_method == ReactionMethod.LLM else "📏 Rules"
        
        st.markdown(
            f'<div style="background-color: #f8f9fa; padding: 12px; border-radius: 6px; margin-bottom: 8px;">'
            f'<strong>Citizen #{citizen.id}</strong> '
            f'<small>({citizen.income_level.value} income, {citizen.political_view.value})</small> '
            f'<span style="float: right; font-size: 0.8em;">{method_badge}</span>'
            f'<br><em>"{state.diary_entry}"</em>'
            f'</div>',
            unsafe_allow_html=True,
        )


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
    
    # Inject custom CSS for modern UI
    inject_custom_css()
    
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
            low_pct_slider = st.slider(
                "Low Income %",
                min_value=0,
                max_value=100,
                value=30,
                step=5,
                help="Percentage of population with low income"
            )
            middle_pct_slider = st.slider(
                "Middle Income %",
                min_value=0,
                max_value=100,
                value=50,
                step=5,
                help="Percentage of population with middle income"
            )
            
            # Calculate high income as remaining percentage
            high_pct_value = 100 - low_pct_slider - middle_pct_slider
            
            # Display high income percentage
            if high_pct_value >= 0:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                            color: white; padding: 12px 20px; border-radius: 12px; 
                            text-align: center; font-weight: 600; margin-top: 10px;">
                    💰 High Income: {high_pct_value}%
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ Low + Middle cannot exceed 100%")
            
            # Convert to 0-1 range for internal use
            low_pct = low_pct_slider / 100.0
            middle_pct = middle_pct_slider / 100.0
            high_pct = max(0.0, high_pct_value / 100.0)
        
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
            width='stretch',
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
        
        st.divider()
        
        # ---------------------------------------------------------------------
        # AI Enhancement (Optional)
        # ---------------------------------------------------------------------
        st.subheader("🤖 AI Enhancement")
        
        # Check if LLM client is available
        llm_client = init_llm_client()
        ai_available = llm_client is not None
        
        if not ai_available:
            st.info(
                "ℹ️ **AI not configured**. Set `GEMINI_API_KEY` in `.env` to enable. "
                "The simulation works perfectly without AI."
            )
            ai_enabled = False
            ai_sample_pct = 0.1
            ai_explanations = True
        else:
            st.success("✅ AI is available (Gemini API configured)")
            
            ai_enabled = st.toggle(
                "Enable AI Enhancement",
                value=st.session_state.ai_enabled,
                help="Use LLM to generate nuanced citizen reactions for a sample",
            )
            st.session_state.ai_enabled = ai_enabled
            
            if ai_enabled:
                st.warning(
                    "⚠️ **AI Disclaimer**: AI-generated content is supplementary. "
                    "Results may vary. Rule-based logic remains the foundation."
                )
                
                ai_sample_pct = st.slider(
                    "AI Sample %",
                    min_value=0.01,
                    max_value=0.50,
                    value=0.10,
                    step=0.01,
                    format="%.0f%%",
                    help="Percentage of citizens processed by AI (rest use rules)",
                )
                
                ai_explanations = st.checkbox(
                    "Generate Explanations",
                    value=True,
                    help="Generate short explanations for sampled citizens",
                )
            else:
                ai_sample_pct = 0.1
                ai_explanations = True
        
        st.divider()
        
        # Run Simulation Button
        sim_disabled = st.session_state.population is None
        if st.button(
            "▶️ Run Simulation",
            type="primary",
            disabled=sim_disabled,
            width='stretch',
        ):
            if st.session_state.population is None:
                st.error("Please generate a population first")
            else:
                ai_status_text = " with AI" if ai_enabled else ""
                with st.spinner(f"Running simulation ({simulation_steps} steps{ai_status_text})..."):
                    try:
                        # Create policy
                        policy = Policy(
                            title=policy_title,
                            description=policy_description,
                            domain=PolicyDomain(policy_domain),
                        )
                        
                        # Create simulation config with AI settings
                        sim_config = SimulationConfig(
                            mode=SimulationMode.BALANCED if ai_enabled else SimulationMode.SPEED,
                            steps=simulation_steps,
                            ai_enabled=ai_enabled,
                            ai_sample_pct=ai_sample_pct,
                            ai_explanation_enabled=ai_explanations,
                        )
                        
                        # Generate scenario name
                        scenario_name = f"{policy_title[:30]} - Step {len(st.session_state.scenarios) + 1}"
                        
                        # Create fresh RNG for simulation
                        pop_config = st.session_state.population_config
                        rng = create_rng(pop_config.random_seed)
                        
                        # Run simulation with optional LLM client
                        result = run_simulation(
                            policy=policy,
                            citizens=st.session_state.population,
                            initial_states=st.session_state.initial_states,
                            config=sim_config,
                            population_config=pop_config,
                            scenario_name=scenario_name,
                            rng=rng,
                            llm_client=llm_client if ai_enabled else None,
                        )
                        
                        # Store result
                        st.session_state.simulation_result = result
                        st.session_state.scenarios[scenario_name] = result
                        
                        # Log AI status
                        if result.ai_status:
                            logger.info(
                                f"Simulation complete: {scenario_name} | "
                                f"AI: {result.ai_status.ai_successes} successes, "
                                f"{result.ai_status.ai_failures} fallbacks"
                            )
                        else:
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
    
    # Modern Header
    st.markdown("""
    <div class="gradient-header">
        <h1 style="margin: 0; font-size: 3rem;">🎯 PolicyPulse</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.95;">
            AI-Powered Policy Impact Simulation & Analysis Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                padding: 15px 20px; border-radius: 10px; border-left: 4px solid #f59e0b; margin-bottom: 20px;">
        <strong>⚠️ Synthetic Simulation Disclaimer:</strong> This tool creates fictional scenarios 
        for exploratory purposes. Results do not predict real-world behavior. Use as a thought experiment 
        to identify potential blind spots—not as a substitute for real data, surveys, or expert analysis.
    </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # Tabbed Navigation Interface  
    # =========================================================================
    
    # Create tabs based on available data
    if st.session_state.simulation_result is not None and st.session_state.population is not None:
        # Full dashboard with all tabs
        tabs = st.tabs([
            "📊 Overview",
            "👥 Demographics",
            "👤 Citizens",
            "� Groups",
            "🎓 Experts",
            "�📈 Time Series",
            "📉 Analytics",
            "🤖 AI Insights",
            "📂 Scenarios"
        ])
        
        result = st.session_state.simulation_result
        
        # Tab 1: Overview
        with tabs[0]:
            render_overview_tab(result)
        
        # Tab 2: Demographics
        with tabs[1]:
            render_demographics_tab(result)
        
        # Tab 3: Citizens
        with tabs[2]:
            render_citizens_tab(result)
        
        # Tab 4: Groups
        with tabs[3]:
            render_groups_tab(result)
        
        # Tab 5: Experts
        with tabs[4]:
            render_experts_tab(result)
        
        # Tab 6: Time Series
        with tabs[5]:
            render_time_series_tab(result)
        
        # Tab 7: Analytics
        with tabs[6]:
            render_analytics_tab(result)
        
        # Tab 8: AI Insights
        with tabs[7]:
            render_ai_insights_tab(result)
        
        # Tab 9: Scenarios
        with tabs[8]:
            render_scenarios_comparison_tab()
    
    elif st.session_state.population is not None:
        # Only population - show 2 tabs
        tabs = st.tabs(["👥 Population", "💡 Get Started"])
        
        with tabs[0]:
            render_population_tab()
        
        with tabs[1]:
            render_getting_started_tab()
    
    else:
        # Welcome screen - no tabs
        render_getting_started_tab()
    
    # Debug info
    if config.debug:
        with st.expander("🐛 Debug Information", expanded=False):
            st.json({
                "project_root": str(PROJECT_ROOT),
                "debug_mode": config.debug,
                "population_generated": st.session_state.population is not None,
                "population_size": len(st.session_state.population) if st.session_state.population else 0,
                "simulation_run": st.session_state.simulation_result is not None,
                "scenarios_count": len(st.session_state.scenarios),
            })
    
    logger.debug("Application render complete")


# =============================================================================
# Tab Rendering Functions
# =============================================================================

def render_overview_tab(result: SimulationResult):
    """Render Overview tab with key metrics and charts."""
    st.markdown('<div class="section-header">📊 Simulation Overview</div>', unsafe_allow_html=True)
    
    summary = get_simulation_summary(result)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if summary['happiness_change'] >= 0 else "inverse"
        st.metric(
            "😊 Avg Happiness",
            format_percentage(summary['final_happiness']),
            delta=format_percentage(summary['happiness_change'], include_sign=True),
            delta_color=delta_color
        )
    
    with col2:
        st.metric(
            "💰 Avg Income",
            format_currency(summary["final_income"]),
            delta=format_currency(summary["income_change"])
        )
    
    with col3:
        support_color = "normal" if summary['support_change'] >= 0 else "inverse"
        st.metric(
            "👍 Policy Support",
            format_percentage(summary["final_support"], include_sign=True),
            delta=format_percentage(summary['support_change'], include_sign=True),
            delta_color=support_color
        )
    
    with col4:
        gap_color = "inverse" if summary["gap_change"] > 0 else "normal"
        st.metric(
            "📊 Happiness Gap",
            format_percentage(summary["final_gap"]),
            delta=format_percentage(summary['gap_change'], include_sign=True),
            delta_color=gap_color
        )
    
    st.divider()
    
    # Policy Details Card
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #667eea; margin-top: 0;">📋 Policy Details</h3>
        <p><strong>Title:</strong> {summary['policy_title']}</p>
        <p><strong>Domain:</strong> <span class="badge badge-info">{summary['policy_domain']}</span></p>
        <p><strong>Scenario:</strong> {summary['scenario_name']}</p>
        <p><strong>Steps:</strong> {summary['steps']} | <strong>Population:</strong> {summary['population_size']:,} citizens</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick Charts
    st.markdown("### 📈 Key Trends")
    render_time_series_charts(result, key_prefix="overview_")


def render_demographics_tab(result: SimulationResult):
    """Render Demographics tab with population breakdown."""
    st.markdown('<div class="section-header">👥 Demographic Analysis</div>', unsafe_allow_html=True)
    
    render_demographic_breakdown(result)
    
    st.divider()
    
    st.markdown("### 📊 Inequality Evolution")
    render_happiness_gap_evolution(result, key_prefix="demographics_")
    
    st.divider()
    
    # Detailed breakdown
    with st.expander("📋 Detailed Population Breakdown", expanded=False):
        summary = get_population_summary(result.citizens)
        render_population_summary(summary)
        render_distribution_charts(summary)


def render_time_series_tab(result: SimulationResult):
    """Render Time Series tab with evolution charts."""
    st.markdown('<div class="section-header">📈 Time Series Analysis</div>', unsafe_allow_html=True)
    
    render_time_series_charts(result, key_prefix="timeseries_")
    
    st.divider()
    
    st.markdown("### 📊 Happiness Trajectories")
    render_happiness_gap_evolution(result, key_prefix="timeseries_")
    
    st.divider()
    
    # Additional metrics table
    st.markdown("### 📋 Step-by-Step Metrics")
    
    metrics_data = []
    for m in result.metrics_by_step:
        metrics_data.append({
            "Step": m.step,
            "Avg Happiness": f"{m.avg_happiness:.1%}",
            "Avg Support": f"{m.avg_support:+.1%}",
            "Avg Income": format_currency(m.avg_income),
            "Happiness Gap": f"{m.happiness_gap:.1%}",
        })
    
    df_metrics = pd.DataFrame(metrics_data)
    st.dataframe(df_metrics, width='stretch', hide_index=True)


def render_citizens_tab(result: SimulationResult):
    """Render Citizens tab."""
    st.markdown('<div class="section-header">👤 Citizens Deep Dive</div>', unsafe_allow_html=True)
    
    final_step = result.config.steps
    final_states = result.states_by_step.get(final_step, [])
    initial_states = result.states_by_step.get(0, [])
    
    final_state_map = {s.citizen_id: s for s in final_states}
    initial_state_map = {s.citizen_id: s for s in initial_states}
    
    st.markdown(f"**Total Citizens: {len(result.citizens):,}**")
    
    detailed_data = []
    for c in result.citizens[:100]:
        if c.id in final_state_map and c.id in initial_state_map:
            initial = initial_state_map[c.id]
            final = final_state_map[c.id]
            detailed_data.append({
                "ID": c.id,
                "Age": c.age,
                "Income Level": c.income_level.value,
                "Zone": c.city_zone.value,
                "Political": c.political_view.value,
                "Final Happiness": final.happiness,
                "Happiness Δ": final.happiness - initial.happiness,
                "Support": final.policy_support,
            })
    
    if detailed_data:
        df_detailed = pd.DataFrame(detailed_data)
        st.dataframe(
            df_detailed.style.format({
                "Final Happiness": "{:.1%}",
                "Happiness Δ": "{:+.1%}",
                "Support": "{:+.1%}",
            }),
            width='stretch',
            hide_index=True
        )


def render_groups_tab(result: SimulationResult):
    """Render Groups tab."""
    st.markdown('<div class="section-header">👔 Group Analysis</div>', unsafe_allow_html=True)
    
    final_metrics = result.metrics_by_step[-1]
    initial_metrics = result.metrics_by_step[0]
    
    # Get final and initial states for additional groupings
    final_states = result.states_by_step.get(result.config.steps, [])
    initial_states = result.states_by_step.get(0, [])
    
    # Create lookup maps
    citizen_map = {c.id: c for c in result.citizens}
    final_state_map = {s.citizen_id: s for s in final_states}
    initial_state_map = {s.citizen_id: s for s in initial_states}
    
    # Calculate happiness by zone and political view
    happiness_by_zone = {zone: [] for zone in CityZone}
    happiness_by_political = {view: [] for view in PoliticalView}
    initial_happiness_by_zone = {zone: [] for zone in CityZone}
    initial_happiness_by_political = {view: [] for view in PoliticalView}
    
    for citizen in result.citizens:
        if citizen.id in final_state_map and citizen.id in initial_state_map:
            final_state = final_state_map[citizen.id]
            initial_state = initial_state_map[citizen.id]
            
            happiness_by_zone[citizen.city_zone].append(final_state.happiness)
            happiness_by_political[citizen.political_view].append(final_state.happiness)
            initial_happiness_by_zone[citizen.city_zone].append(initial_state.happiness)
            initial_happiness_by_political[citizen.political_view].append(initial_state.happiness)
    
    # Calculate averages
    avg_happiness_by_zone = {
        zone: sum(vals) / len(vals) if vals else 0
        for zone, vals in happiness_by_zone.items()
    }
    avg_happiness_by_political = {
        view: sum(vals) / len(vals) if vals else 0
        for view, vals in happiness_by_political.items()
    }
    initial_avg_happiness_by_zone = {
        zone: sum(vals) / len(vals) if vals else 0
        for zone, vals in initial_happiness_by_zone.items()
    }
    initial_avg_happiness_by_political = {
        view: sum(vals) / len(vals) if vals else 0
        for view, vals in initial_happiness_by_political.items()
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**💰 Income Groups**")
        for level in IncomeLevel:
            final_h = final_metrics.happiness_by_income.get(level, 0)
            initial_h = initial_metrics.happiness_by_income.get(level, 0)
            change = final_h - initial_h
            st.metric(level.value, f"{final_h:.1%}", f"{change:+.1%}")
    
    with col2:
        st.markdown("**🏘️ City Zones**")
        for zone in CityZone:
            final_h = avg_happiness_by_zone.get(zone, 0)
            initial_h = initial_avg_happiness_by_zone.get(zone, 0)
            change = final_h - initial_h
            st.metric(zone.value, f"{final_h:.1%}", f"{change:+.1%}")
    
    with col3:
        st.markdown("**🗳️ Political Views**")
        for view in PoliticalView:
            final_h = avg_happiness_by_political.get(view, 0)
            initial_h = initial_avg_happiness_by_political.get(view, 0)
            change = final_h - initial_h
            st.metric(view.value, f"{final_h:.1%}", f"{change:+.1%}")


def render_experts_tab(result: SimulationResult):
    """Render Experts tab."""
    st.markdown('<div class="section-header">🎓 Expert Analysis</div>', unsafe_allow_html=True)
    
    summary = get_simulation_summary(result)
    
    happiness_score = (summary['happiness_change'] + 0.5) * 50
    support_score = (summary['final_support'] + 1) * 25
    composite_score = min(100, max(0, happiness_score + support_score))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Composite Score", f"{composite_score:.0f}/100")
        st.progress(composite_score / 100)
    
    with col2:
        grade = "A" if composite_score >= 80 else "B" if composite_score >= 70 else "C" if composite_score >= 60 else "D" if composite_score >= 50 else "F"
        st.metric("Policy Grade", grade)
    
    with col3:
        effectiveness = "High" if composite_score >= 80 else "Moderate" if composite_score >= 60 else "Limited"
        st.metric("Effectiveness", effectiveness)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ Strengths**")
        if summary['happiness_change'] > 0:
            st.success(f"Happiness increased by {summary['happiness_change']:.1%}")
        if summary['final_support'] > 0:
            st.success(f"Positive support: {summary['final_support']:+.1%}")
    
    with col2:
        st.markdown("**⚠️ Concerns**")
        if summary['happiness_change'] < 0:
            st.warning(f"Happiness declined by {summary['happiness_change']:.1%}")
        if summary['gap_change'] > 0.1:
            st.warning(f"Inequality increased by {summary['gap_change']:.1%}")


def render_analytics_tab(result: SimulationResult):
    """Render Analytics tab."""
    st.markdown('<div class="section-header">📉 Advanced Analytics</div>', unsafe_allow_html=True)
    
    final_states = result.states_by_step.get(result.config.steps, [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        happiness_values = [s.happiness * 100 for s in final_states]
        fig = go.Figure(data=[go.Histogram(
            x=happiness_values,
            nbinsx=30,
            marker_color='#667eea'
        )])
        fig.update_layout(title="Happiness Distribution", height=300)
        st.plotly_chart(fig, key="analytics_happiness", width='stretch')
    
    with col2:
        support_values = [s.policy_support * 100 for s in final_states]
        fig = go.Figure(data=[go.Histogram(
            x=support_values,
            nbinsx=30,
            marker_color='#764ba2'
        )])
        fig.update_layout(title="Support Distribution", height=300)
        st.plotly_chart(fig, key="analytics_support", width='stretch')
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Happiness Stats**")
        st.metric("Mean", f"{sum(happiness_values)/len(happiness_values):.1f}%")
        st.metric("Std Dev", f"{pd.Series(happiness_values).std():.1f}%")
    
    with col2:
        st.markdown("**Support Stats**")
        st.metric("Mean", f"{sum(support_values)/len(support_values):+.1f}%")
        positive_pct = sum(1 for s in support_values if s > 0) / len(support_values) * 100
        st.metric("Positive %", f"{positive_pct:.0f}%")
    
    with col3:
        st.markdown("**Volatility**")
        vol = pd.Series([m.avg_happiness for m in result.metrics_by_step]).std() * 100
        st.metric("Happiness Vol", f"{vol:.2f}%")


def render_ai_insights_tab(result: SimulationResult):
    """Render AI Insights tab."""
    st.markdown('<div class="section-header">🤖 AI Integration & Insights</div>', unsafe_allow_html=True)
    
    render_ai_status(result)
    
    st.divider()
    
    if result.config.ai_explanation_enabled:
        render_sample_explanations(result, max_samples=10)
    else:
        st.info("💡 AI explanations were not enabled for this simulation. Enable them in the sidebar for AI-generated insights.")


def render_scenarios_comparison_tab():
    """Render Scenarios comparison tab."""
    st.markdown('<div class="section-header">📂 Scenario Comparison</div>', unsafe_allow_html=True)
    
    if len(st.session_state.scenarios) == 0:
        st.info("ℹ️ No saved scenarios yet. Run multiple simulations to compare them here.")
        return
    
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10b981;">
        <h4 style="margin-top: 0;">✅ Saved Scenarios: {len(st.session_state.scenarios)}</h4>
        <p>Compare different policy approaches side-by-side</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario selector
    selected_scenarios = st.multiselect(
        "Select scenarios to compare (2-5 recommended)",
        options=list(st.session_state.scenarios.keys()),
        default=list(st.session_state.scenarios.keys())[:min(3, len(st.session_state.scenarios))]
    )
    
    if len(selected_scenarios) >= 2:
        # Build comparison data
        comparison_data = []
        for name in selected_scenarios:
            result = st.session_state.scenarios[name]
            summary = get_simulation_summary(result)
            comparison_data.append({
                "Scenario": name,
                "Policy": summary["policy_title"],
                "Domain": summary["policy_domain"],
                "Population": summary["population_size"],
                "Steps": summary["steps"],
                "Happiness Δ": summary["happiness_change"],
                "Income Δ": summary["income_change"],
                "Support Δ": summary["support_change"],
                "Gap Δ": summary["gap_change"],
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        
        st.markdown("### 📊 Comparison Table")
        st.dataframe(
            df_comparison.style.format({
                "Population": "{:,}",
                "Happiness Δ": "{:+.1%}",
                "Income Δ": "${:+,.0f}",
                "Support Δ": "{:+.1%}",
                "Gap Δ": "{:+.1%}",
            }),
            width='stretch',
            hide_index=True
        )
        
        st.divider()
        
        # Comparison Charts
        st.markdown("### 📈 Visual Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[go.Bar(
                x=df_comparison["Scenario"],
                y=df_comparison["Happiness Δ"] * 100,
                marker=dict(
                    color=df_comparison["Happiness Δ"],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Change %")
                ),
                text=df_comparison["Happiness Δ"].apply(lambda x: f"{x:+.1%}"),
                textposition='outside'
            )])
            fig.update_layout(
                title="Happiness Change Comparison",
                xaxis_title="Scenario",
                yaxis_title="Change (%)",
                height=400,
                margin=dict(t=40, b=40, l=40, r=40)
            )
            st.plotly_chart(fig, key="scenario_happiness_comparison", width='stretch')
        with col2:
            fig = go.Figure(data=[go.Bar(
                x=df_comparison["Scenario"],
                y=df_comparison["Support Δ"] * 100,
                marker=dict(
                    color=df_comparison["Support Δ"],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Change %")
                ),
                text=df_comparison["Support Δ"].apply(lambda x: f"{x:+.1%}"),
                textposition='outside'
            )])
            fig.update_layout(
                title="Support Change Comparison",
                xaxis_title="Scenario",
                yaxis_title="Change (%)",
                height=400,
                margin=dict(t=40, b=40, l=40, r=40)
            )
            st.plotly_chart(fig, key="scenario_support_comparison", width='stretch')
        # Income comparison
        fig = go.Figure(data=[go.Bar(
            x=df_comparison["Scenario"],
            y=df_comparison["Income Δ"],
            marker_color='#667eea',
            text=df_comparison["Income Δ"].apply(lambda x: f"${x:+,.0f}"),
            textposition='outside'
        )])
        fig.update_layout(
            title="Income Change Comparison",
            xaxis_title="Scenario",
            yaxis_title="Income Change ($)",
            height=400,
            margin=dict(t=40, b=40, l=40, r=40)
        )
        st.plotly_chart(fig, key="scenario_income_comparison", width='stretch')
    
    elif len(selected_scenarios) == 1:
        st.warning("⚠️ Select at least 2 scenarios to see comparisons")


def render_population_tab():
    """Render Population tab when only population exists."""
    st.markdown('<div class="section-header">👥 Population Overview</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card" style="border-left-color: #10b981;">
        <h4 style="margin-top: 0;">✅ Population Ready</h4>
        <p>Your synthetic population has been generated. Configure a policy in the sidebar and click 
        <strong>Run Simulation</strong> to see how it affects different groups!</p>
    </div>
    """, unsafe_allow_html=True)
    
    population = st.session_state.population
    initial_states = st.session_state.initial_states
    
    summary = get_population_summary(population)
    render_population_summary(summary)
    
    st.divider()
    
    render_distribution_charts(summary)
    
    st.divider()
    
    # Initial State Metrics
    initial_metrics = calculate_step_metrics(population, initial_states, step=0)
    st.markdown("### 📊 Initial State Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Happiness", format_percentage(initial_metrics.avg_happiness))
    with col2:
        st.metric("Avg Support", format_percentage(initial_metrics.avg_support, include_sign=True))
    with col3:
        st.metric("Avg Income", format_currency(initial_metrics.avg_income))
    with col4:
        st.metric("Happiness Gap", format_percentage(initial_metrics.happiness_gap))
    
    st.divider()
    
    render_citizens_preview(population, initial_states, max_rows=20)


def render_getting_started_tab():
    """Render Getting Started / Welcome tab."""
    st.markdown('<div class="section-header">👋 Welcome to PolicyPulse</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card" style="border-left-color: #3b82f6;">
        <h3 style="margin-top: 0;">🚀 Get Started in Two Steps</h3>
        <ol style="font-size: 1.1rem; line-height: 1.8;">
            <li><strong>Generate a Population</strong> - Use the sidebar to create 100-50,000 synthetic citizens</li>
            <li><strong>Run a Simulation</strong> - Configure a policy and see how it affects different groups</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🎯 What You'll Discover")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Comprehensive Metrics</h4>
            <ul>
                <li>Happiness & income changes</li>
                <li>Policy support levels</li>
                <li>Inequality gap tracking</li>
                <li>Demographic breakdowns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Time Series Analysis</h4>
            <ul>
                <li>Evolution over multiple steps</li>
                <li>Trend visualization</li>
                <li>Group trajectories</li>
                <li>Interactive charts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>👥 Demographic Insights</h4>
            <ul>
                <li>Income level comparisons</li>
                <li>Political view analysis</li>
                <li>City zone differences</li>
                <li>Inequality measures</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h4>🤖 AI Enhancement</h4>
            <ul>
                <li>Nuanced citizen reactions</li>
                <li>Explanatory insights</li>
                <li>Pattern detection</li>
                <li>Scenario summaries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 💡 Understanding Policy Domains")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #8b5cf6;">
            <h4>🏦 Economy</h4>
            <p>Tax cuts, interest rates, trade policies. Often favor higher income groups.</p>
        </div>
        
        <div class="metric-card" style="border-left-color: #8b5cf6;">
            <h4>📚 Education</h4>
            <p>School funding, training programs. Typically help lower income groups most.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #8b5cf6;">
            <h4>🤝 Social</h4>
            <p>Healthcare, housing, welfare. Strong impact on vulnerable populations.</p>
        </div>
        
        <div class="metric-card" style="border-left-color: #8b5cf6;">
            <h4>💼 Business</h4>
            <p>Deregulation, incentives, subsidies. Usually benefit business owners.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
