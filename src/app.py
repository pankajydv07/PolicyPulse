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
)


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
    # Initialize
    init_session_state()
    load_persisted_data()
    
    # TODO: Render header
    
    # TODO: Render sidebar
    # - Population config
    # - Simulation config
    # - Policy config
    # - Action buttons
    # - Learning status
    
    # TODO: Handle simulation run
    
    # TODO: Render main content
    # - Welcome state (if no simulation)
    # - Disclaimer
    # - Tabs with content
    
    # Placeholder until UI is implemented
    st.title("🎯 PolicyPulse")
    st.info("Application scaffolding complete. UI implementation pending.")
    
    # Show configuration status
    config = get_config()
    if config.has_api_key:
        st.success("✅ Gemini API key configured")
    else:
        st.warning("⚠️ No Gemini API key found. Set GEMINI_API_KEY in .env file.")
    
    st.caption("Run with: `streamlit run src/app.py`")


if __name__ == "__main__":
    main()
