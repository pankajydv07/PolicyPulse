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
    # TODO: Initialize session state keys
    # - scenarios: dict of SimulationResult
    # - current_population: list of Citizens
    # - current_states: list of CitizenState
    # - nn_model: NeuralNetworkModel instance
    # - training_data: TrainingDataManager instance
    # - llm_client: LLMClient instance (or None)
    # - selected_scenario: str
    # - selected_citizen_id: int | None
    pass


def load_persisted_data() -> None:
    """
    Load persisted models and training data from disk.
    
    Reference: TECH_STACK.md Section 8 (Persistence Lifecycle)
    """
    # TODO: Load trained model if exists
    # TODO: Load training samples if exist
    pass


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
    # Sidebar (placeholder)
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
        
        st.subheader("Simulation")
        steps = st.slider(
            "Time Steps",
            min_value=1,
            max_value=10,
            value=config.default_simulation_steps,
            help="Number of simulation steps to run",
        )
        
        mode = st.selectbox(
            "Mode",
            options=["Precision", "Balanced", "Speed"],
            index=1,
            help="Precision: LLM only | Balanced: Hybrid | Speed: NN only",
        )
        
        st.subheader("Policy")
        policy_title = st.text_input("Policy Title", value="Example Policy")
        policy_domain = st.selectbox(
            "Domain",
            options=["Economy", "Education", "Social", "Business"],
        )
        
        st.divider()
        
        run_disabled = not config.has_api_key and mode != "Speed"
        if st.button("▶️ Run Simulation", type="primary", disabled=run_disabled, use_container_width=True):
            st.info("Simulation not yet implemented")
            logger.info(f"Simulation requested: {population_size} citizens, {steps} steps, {mode} mode")
        
        if run_disabled:
            st.caption("⚠️ API key required for Precision/Balanced modes")
    
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
    
    # Welcome state (no simulation run yet)
    st.markdown("### 👋 Welcome to PolicyPulse")
    st.markdown(
        """
        Get started in three steps:
        
        1. **Configure a policy** in the sidebar
        2. **Choose a simulation mode** (Balanced recommended for first run)
        3. **Click "Run Simulation"** to see results
        """
    )
    
    with st.expander("💡 Tip: Understanding Simulation Modes"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🎯 Precision Mode**")
            st.markdown("Uses AI (LLM) for every citizen reaction. Slower but highest quality.")
        with col2:
            st.markdown("**⚖️ Balanced Mode**")
            st.markdown("Samples citizens for AI, scales with neural network. Best of both worlds.")
        with col3:
            st.markdown("**⚡ Speed Mode**")
            st.markdown("Uses trained neural network only. Fast, works offline after training.")
    
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
        if TRAINING_DATA_PATH.exists():
            st.success("✅ Training Data: Available")
        else:
            st.info("ℹ️ Training Data: None")
    
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
            })
    
    logger.debug("Application render complete")


if __name__ == "__main__":
    main()
