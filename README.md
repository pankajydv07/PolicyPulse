# PolicyPulse

🎯 **AI-powered synthetic population simulator for stress-testing policies**

## What is PolicyPulse?

PolicyPulse is an intelligent simulation platform that helps organizations, governments, and researchers test the impact of policies before implementing them in the real world. By creating synthetic populations of virtual citizens with realistic demographic distributions, PolicyPulse simulates how different groups respond to proposed policies over time.

## What Does It Do?

PolicyPulse enables you to:

- **Simulate Policy Impact**: Test how policies affect different demographic groups (income levels, political views, city zones)
- **Predict Population Response**: Understand how citizens' happiness, income, and behavior change over multiple time steps
- **Compare Scenarios**: Run multiple policy simulations side-by-side to choose the best option
- **Analyze Inequalities**: Track wealth gaps, income distribution, and demographic disparities
- **Get Expert Insights**: Receive AI-generated analysis from economist, activist, and business perspectives

## How Does It Work?

PolicyPulse uses a hybrid AI approach that combines:

1. **Synthetic Population Generation**: Creates virtual citizens with diverse attributes (age, income, education, political views, location)
2. **Policy Analysis**: Uses AI (Google Gemini LLM) to understand policy text and predict expected impacts
3. **Simulation Engine**: Three simulation modes:
   - **Precision Mode**: LLM-powered reactions for maximum accuracy (slower)
   - **Balanced Mode**: Hybrid approach - LLM for sampling + neural network for scaling (optimal)
   - **Speed Mode**: Pure neural network predictions (fast, offline-capable)
4. **Analytics Dashboard**: Interactive visualizations showing time-series data, demographic breakdowns, and inequality metrics

## Main Use Cases

- **Government Policy Testing**: Evaluate tax reforms, welfare programs, housing policies before implementation
- **Corporate Strategy**: Test employee policies, benefit changes, or organizational initiatives
- **Research & Education**: Study policy impacts, demographic responses, and social dynamics
- **Urban Planning**: Simulate zoning changes, transportation policies, or development plans
- **Social Impact Analysis**: Understand how policies affect different communities and reduce inequalities

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Git
- Google Gemini API key (free tier available - for Precision/Balanced modes)

### Installation

**Step 1: Clone the Repository**

```bash
git clone https://github.com/yourusername/PolicyPulse.git
cd PolicyPulse
```

**Step 2: Create Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Requirements**

```bash
pip install -r requirements.txt
```

**Step 4: Configure Environment (Optional for Speed Mode)**

Create a `.env` file in the project root:

```bash
# Windows
echo GEMINI_API_KEY=your_api_key_here > .env

# Linux/Mac
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Get your free API key from: https://makersuite.google.com/app/apikey

**Note**: API key is only required for Precision and Balanced modes. Speed Mode works offline without an API key.

### Running the Application

```bash
# Windows
set PYTHONPATH=%cd%
streamlit run src/app.py

# Linux/Mac
export PYTHONPATH=$(pwd)
streamlit run src/app.py
```

Or use this single command that works on all platforms:

```bash
python -m streamlit run src/app.py
```

The application will automatically open in your browser at `http://localhost:8501`.

### Using PolicyPulse

1. **Configure Population**: Set population size (100-50,000 citizens) and demographic distribution
2. **Enter Policy**: Describe the policy you want to test (e.g., "Increase minimum wage by 20%")
3. **Choose Simulation Mode**: 
   - Speed Mode: Fast, no API needed
   - Balanced Mode: Best accuracy/speed tradeoff
   - Precision Mode: Maximum accuracy
4. **Run Simulation**: Watch the simulation progress through multiple time steps
5. **Analyze Results**: Review charts, statistics, and AI-generated expert perspectives
6. **Compare Scenarios**: Save results and compare different policy options

## Project Structure

```
PolicyPulse/
├── data/
│   └── README.md            # Training data storage
├── models/
│   └── README.md            # Trained model storage
├── src/
│   ├── app.py               # Main Streamlit application
│   ├── config.py            # Environment configuration
│   ├── data_models.py       # Dataclass definitions (Citizen, Policy, etc.)
│   ├── llm_client.py        # Google Gemini API wrapper
│   ├── logging_config.py    # Logging configuration
│   ├── ml_data.py           # Training data management
│   ├── nn_model.py          # Neural network model
│   ├── policy_analyzer.py   # LLM-based policy analysis
│   ├── population.py        # Population generation
│   ├── rl_trainer.py        # Reinforcement learning trainer
│   ├── simulation.py        # Simulation orchestration
│   ├── stats.py             # Statistics and aggregation
│   └── utils.py             # Utility functions
├── tests/
│   ├── test_data_models.py  # Unit tests for data models
│   ├── test_llm_client.py   # LLM client tests
│   ├── test_nn_model.py     # Neural network tests
│   ├── test_population.py   # Population generation tests
│   ├── test_simulation.py   # Simulation tests
│   ├── test_stats.py        # Statistics tests
│   └── test_utils.py        # Utility function tests
├── .env                     # Environment variables (create from .env.example)
├── .gitignore               # Git ignore rules
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── TECH_STACK.md            # Technology Architecture
└── SKILL.md                 # AI coding assistant guidelines
```

## Architecture

PolicyPulse follows a **modular monolith** pattern:

- **UI Layer** (`app.py`): Streamlit web interface with session management
- **Simulation Engine** (`simulation.py`): Orchestrates the hybrid AI workflow
- **AI Modules** (`llm_client.py`, `policy_analyzer.py`, `nn_model.py`): LLM and neural network integration
- **Population System** (`population.py`): Generates synthetic citizens with realistic demographics
- **Data Layer** (`data_models.py`, `ml_data.py`, `stats.py`): Data structures, training data, and analytics

## Key Technologies

- **Python 3.10+**: Core language with type hints and dataclasses
- **Streamlit**: Web framework for rapid UI development
- **Google Gemini API**: LLM for policy analysis and citizen reactions
- **Scikit-learn**: Neural network for fast predictions
- **Pandas & NumPy**: Data processing and numerical computations
- **Plotly**: Interactive data visualizations

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_simulation.py
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For questions, issues, or feature requests, please:
- Open an issue on GitHub
- Check existing documentation in TECH_STACK.md and SKILL.md
- Review test files for usage examples

## Acknowledgments

Built with modern Python tools and AI technologies to democratize policy impact analysis.

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Type Checking

```bash
mypy src/
```

### Code Style

The project uses Python 3.10+ type hints throughout. All functions should have complete type annotations.

## Documentation

- [PRD.md](PRD.md) - Product Requirements Document
- [DESIGN_DOC.md](DESIGN_DOC.md) - UI/UX Design Specification
- [TECH_STACK.md](TECH_STACK.md) - Technology Architecture Decisions
- [SKILL.md](SKILL.md) - AI Coding Assistant Guidelines

## Disclaimer

⚠️ **Synthetic Simulation Disclaimer**

This tool creates fictional scenarios for exploratory purposes. Results do not predict real-world behavior. Use as a thought experiment to identify potential blind spots—not as a substitute for real data, surveys, or expert analysis.

## License

MIT License
