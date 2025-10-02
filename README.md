# LUNTRA Calculator MVP

**Deal calculator for house-hack & whole unit models with PDF export and financial heuristics**

A 60-second deal analysis tool built with Streamlit for real estate investment calculations. This MVP is part of the LUNTRA paid beta sprint, providing rapid financial analysis for both house-hack and whole unit rental property models.

## Features

- 🏠 **Dual Calculation Models**: House-hack and whole unit analysis
- ⚡ **60-Second Analysis**: Quick input and instant results
- 📄 **PDF Export**: Generate professional deal reports
- 📊 **Financial Heuristics**: Built-in investment rules and ratios
- 🔧 **Streamlit UI**: Interactive web-based interface
- 📈 **Session Telemetry**: Track usage and configurations

## Quick Start

### 1. Environment Setup

```bash
# Clone or navigate to the project directory
cd luntra-calculator-mvp

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Start the Streamlit app
streamlit run app.py

# The app will open in your browser at http://localhost:8501
```

### 3. Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload for development
streamlit run app.py --server.runOnSave true
```

## Project Structure

```
luntra-calculator-mvp/
├── app.py                 # Main Streamlit application entry point
├── requirements.txt       # Python dependencies
├── venv/                 # Virtual environment (auto-created)
├── calculator/           # Core calculation modules
├── tests/                # Unit tests
├── sample_data/          # Sample deal data for testing
└── README.md             # This file
```

## Usage

1. **Select Model**: Choose between "House-Hack" or "Whole Unit" in the sidebar
2. **Input Deal Parameters**: 
   - Purchase price
   - Down payment percentage
   - Interest rate
3. **View Analysis**: Real-time financial calculations and heuristics
4. **Export PDF**: Generate professional deal summary reports
5. **Save/Load**: Manage deal configurations

## Financial Models

### House-Hack Model
- Owner-occupied investment property analysis
- Reduced down payment requirements (3-5%)
- Personal residence tax benefits
- Rental income from additional units

### Whole Unit Model
- Traditional rental property analysis
- Standard investment property financing (20-25% down)
- Full rental income analysis
- Complete expense calculations

## Development

### Environment Variables

Create a `.env` file for configuration:

```bash
# Optional: Custom configuration
STREAMLIT_SERVER_PORT=8501
DEBUG_MODE=true
```

### Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=calculator tests/
```

### Code Formatting

```bash
# Format code
black app.py calculator/

# Lint code
flake8 app.py calculator/
```

## Deployment

### Local Development
- Use `streamlit run app.py`
- Automatic reload on file changes

### Production Deployment
- Deploy to Streamlit Cloud, Heroku, or similar platform
- Ensure environment variables are properly configured
- Use production-ready configuration

## Integration with LUNTRA System

This MVP integrates with the broader LUNTRA outreach automation system:

- **OUTREACH AGENT**: Backend AI processing and lead enrichment
- **OUTREACH APP**: Main Streamlit frontend and template management
- **OUTREACH PAID BETA**: Serverless functions and health monitoring

## Telemetry and Analytics

The application collects session data for improvement:
- Calculation model usage
- Input parameter distributions  
- Export and save actions
- Session timestamps

All data collection respects user privacy and is used solely for product improvement.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Ensure code formatting with `black`
5. Submit a pull request

## License

Private beta software - All rights reserved LUNTRA 2024

## Support

For beta users experiencing issues:
- Check the troubleshooting section
- Review sample data examples
- Contact beta support team

---

**LUNTRA Calculator MVP** - Part of the paid beta sprint for 60-second deal analysis