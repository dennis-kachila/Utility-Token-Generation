# Utility Token Generation Project

A comprehensive simulation of utility token generation, decryption, and analysis based on Standard Transfer Specification (STS) concepts.

## Overview

This project demonstrates how utility tokens work in prepaid metering systems. It includes components for token generation, decryption, data cleaning, visualization, and a graphical user interface.

## Features

- **Token Generation**: Create 20-digit tokens based on meter number and payment amount
- **Decoder Key Generation**: Generate meter-specific decoder keys using the DKGA02 algorithm
- **Token Decryption**: Decrypt tokens to extract information like units purchased
- **Data Cleaning**: Process raw token data from text files
- **Data Visualization**: Create charts and graphs to analyze token usage patterns
- **Modern GUI Interface**: User-friendly interface for all components

## Project Structure

The project follows a clean, organized structure:

```
Utility Token Generation/
├── main.py                # Main entry point
├── requirements.txt       # Project dependencies
├── run.bat                # Windows runner script
├── run.sh                 # Linux/macOS runner script
├── src/                   # Source code
│   ├── Token.py           # Token generation
│   ├── DKGA02.py          # Decoder key generation
│   ├── TokenDecrypter.py  # Token decryption
│   ├── data_cleaning.py   # Data cleaning
│   ├── TokenVisualizer.py # Data visualization
│   ├── test_components.py # Component testing
│   ├── UtilityTokenGUI.py # Graphical interface
│   └── create_icon.py     # Icon generation
├── resources/             # Resources used by the application
│   ├── data/              # Data files
│   │   ├── cleaned_meter_data.csv
│   │   ├── cleaned_meter_data.xlsx
│   │   ├── Raw-SMS-Meter-tokens.txt
│   │   └── token_summary_statistics.txt
│   └── images/            # Image files
│       ├── icon.ico
│       ├── units_over_time.png
│       ├── amount_distribution.png
│       └── ... (other visualization images)
└── docs/                  # Documentation
    ├── README.md
    ├── QUICKSTART.md
    ├── TECHNICAL_DOCS.md
    └── ... (other documentation)
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/utility-token-generation.git
   cd utility-token-generation
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv utility
   source utility/Scripts/activate  # On Windows: utility\Scripts\activate.bat
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Using the Main Script

The `main.py` script provides a unified interface to all components:

```bash
# Launch GUI interface (default)
python main.py

# Generate a token
python main.py token

# Generate a decoder key
python main.py key

# Decrypt a token
python main.py decrypt

# Process raw token data
python main.py clean

# Visualize token data
python main.py visualize

# Run component tests
python main.py test
```

### Using the Runner Scripts

For convenience, you can use the provided runner scripts:

- On Windows: `run.bat`
- On Linux/macOS: `bash run.sh`

These scripts will present a menu to access all project components.

## Documentation

Detailed documentation is available in the `docs` directory:

- `QUICKSTART.md`: Quick guide to get started
- `TECHNICAL_DOCS.md`: Technical details of the implementation
- `DEMO_SCRIPT.md`: Script for demonstrating the project

## License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## References

- [Standard Transfer Specification (STS)](https://www.sts.org.za/)
- [Demystifying Utility Tokens - Part 1](https://mwangi-patrick.medium.com/lets-demystify-that-20-digit-utility-token-part-1-74c85eebbac4)
- [Demystifying Utility Tokens - Part 2](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-2-64ca45f4b88b)
- [Demystifying Utility Tokens - Part 3](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-3-d05002dbdf71)
- [Demystifying Utility Tokens - Part 4](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-4-9143c1c0792c)