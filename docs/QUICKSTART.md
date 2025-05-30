# Quick Start Guide

This document provides a quick start guide for the Utility Token Generation project.

## Setup

1. **Clone the Repository**
   
   ```bash
   git clone https://github.com/yourusername/utility-token-generation.git
   cd utility-token-generation
   ```

2. **Install Dependencies**
   
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage Flow

### 1. Generate a Vending Key

The vending key is automatically generated the first time you run `DKGA02.py`:

```bash
python DKGA02.py
```

### 2. Generate a Demo Token

```bash
python Token.py
```

When prompted:
- Enter a meter number (e.g., `37194275246`)
- Enter an amount (e.g., `100`)

### 3. Decrypt a Token

```bash
python TokenDecrypter.py
```

When prompted:
- Enter the meter number you used before
- Enter the token that was generated

### 4. Process Raw Token Data

```bash
python data-cleaning.py
```

This will process the raw token data from `Raw-SMS-Meter-tokens.txt` and generate:
- `cleaned_meter_data.csv`
- `cleaned_meter_data.xlsx`

### 5. Visualize Token Data

```bash
python TokenVisualizer.py
```

This will generate several visualization files:
- `units_over_time.png`
- `amount_distribution.png`
- `units_per_amount.png`
- `monthly_spending.png`
- `token_data_dashboard.png`

### 6. Run Component Tests

```bash
python test_components.py
```

This will test the TokenDecrypter and TokenVisualizer components to ensure they're working correctly.

### 7. Launch the GUI Interface

```bash
python UtilityTokenGUI.py
```

This will launch a user-friendly graphical interface that provides access to all project components.

### 8. Using the Runner Scripts

For convenience, you can use the provided runner scripts which offer a menu-based interface:

On Windows:
```cmd
run.bat
```

On Linux/macOS:
```bash
bash run.sh
```

## Example Data

You can use the following example data for testing:

- **Meter Number**: 37194275246
- **Token**: 1865-3776-4842-2132-9404
- **Amount**: 20.00 KSh

## Troubleshooting

- If you encounter issues with missing dependencies, run `pip install -r requirements.txt` again.
- Make sure all files are in the same directory.
- Ensure you have the `Raw-SMS-Meter-tokens.txt` file in the project directory.
