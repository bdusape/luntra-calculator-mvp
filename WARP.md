# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

LUNTRA Calculator MVP is a 60-second deal analysis tool built with Streamlit for real estate investment calculations. This MVP is part of the LUNTRA paid beta sprint, providing rapid financial analysis for both house-hack and whole unit rental property models.

## Common Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the Streamlit app
streamlit run app.py

# Run with auto-reload for development
streamlit run app.py --server.runOnSave true

# Run with custom port
streamlit run app.py --server.port 8502
```

### Testing
```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest --cov=calculator tests/

# Run a single test file
pytest tests/test_specific.py

# Run tests with verbose output
pytest -v tests/
```

### Code Quality
```bash
# Format code with black
black app.py calculator/

# Check formatting without changes
black --check app.py calculator/

# Lint code with flake8
flake8 app.py calculator/

# Run all quality checks
black --check app.py calculator/ && flake8 app.py calculator/
```

### Dependencies
```bash
# Install new package and update requirements
pip install package_name
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## Architecture Overview

### Core Application Structure
- **`app.py`**: Main Streamlit application entry point containing the UI logic and basic calculations
- **`calculator/`**: Core calculation modules (currently empty, intended for financial calculation logic)
- **`tests/`**: Unit tests for the application logic
- **`sample_data/`**: Sample deal data for testing and demonstration
- **`venv/`**: Python virtual environment

### Key Design Patterns
- **Single-file Streamlit app**: Currently all UI and basic logic is in `app.py`
- **Modular calculation design**: Intended separation of calculation logic into `calculator/` modules
- **Session-based telemetry**: Tracks user interactions and configurations in session data
- **Dual model support**: Architecture supports both House-Hack and Whole Unit calculation models

### Financial Models
1. **House-Hack Model**: Owner-occupied investment property analysis with reduced down payments (3-5%)
2. **Whole Unit Model**: Traditional rental property analysis with standard investment financing (20-25% down)

### Data Flow
1. User selects calculation model in sidebar
2. Input parameters (purchase price, down payment %, interest rate) collected via Streamlit widgets
3. Basic calculations performed inline in `app.py`
4. Results displayed in main content area with metrics
5. Session data captured for telemetry
6. PDF export functionality (planned)

### Integration Points
This MVP integrates with the broader LUNTRA system:
- **OUTREACH AGENT**: Backend AI processing and lead enrichment
- **OUTREACH APP**: Main Streamlit frontend and template management  
- **OUTREACH PAID BETA**: Serverless functions and health monitoring

## Development Notes

### Current State
- Basic Streamlit UI is functional with input controls and layout
- Core financial calculations are stubbed out (marked with TODO comments)
- PDF export functionality is planned but not implemented
- Calculator modules are empty and need implementation
- No tests are currently written

### Key TODOs in Codebase
- Implement house-hack specific calculations in `app.py:93`
- Implement whole unit specific calculations in `app.py:97`
- Add PDF export functionality in `app.py:106`
- Implement save/load functionality in `app.py:125,129`
- Build out `calculator/` module structure for financial calculations

### Environment Configuration
- Uses `.env` file for optional configuration (STREAMLIT_SERVER_PORT, DEBUG_MODE)
- Session data includes model type, financial inputs, and timestamps
- Telemetry respects user privacy and is used for product improvement

### File Organization Strategy
The README suggests a future structure with:
- Core calculation modules in `calculator/`
- Unit tests in `tests/`
- Sample data in `sample_data/`
- Currently only the main `app.py` contains implementation

## Streamlit-Specific Notes

### Page Configuration
- Wide layout with expanded sidebar
- Custom page title and icon (🏠)
- Two-column layout with main analysis and export/actions sidebar

### Key UI Components
- Sidebar configuration with model selection and quick inputs
- Main content area with metrics display and analysis results
- Export section with PDF generation and session data viewing
- Session telemetry displayed as expandable JSON

### State Management
- Uses Streamlit's native state management
- Session data stored in Python dictionaries
- Configuration parameters controlled via Streamlit widgets (selectbox, slider, number_input)