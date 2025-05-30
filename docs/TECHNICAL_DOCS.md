# Utility Token Generation - Technical Documentation

## Introduction

This document provides detailed technical information about the Utility Token Generation project, which implements a simplified version of the Standard Transfer Specification (STS) for prepaid utility tokens. The STS is a global standard for secure transfer of credits in prepaid metering systems.

## System Architecture

The project is designed with a modular architecture consisting of several key components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Token Generator │────>│ Token Decrypter │────>│ Data Processor  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         ▼                      ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  DKGA02 Module  │     │ TokenVisualizer │<────│  Data Cleaning  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       
         │                      │                       
         ▼                      ▼                       
┌─────────────────┐     ┌─────────────────┐     
│   Vending Key   │     │  GUI Interface  │     
└─────────────────┘     └─────────────────┘     
```

## Component Details

### 1. Token Generation (`Token.py`)

The token generation process simulates how a utility provider would generate a token based on a customer's meter number and payment amount.

#### Key Functions:

- `generate_demo_token(meter_number, amount)`: Generates a 20-digit token for the given meter number and amount.
- `format_token(token)`: Formats the token with separators for better readability.

#### Algorithm Overview:

1. Calculate the number of units based on the payment amount
2. Generate a random token identifier (TID)
3. Combine the meter number, amount, and TID into a data block
4. Encrypt the data block using a cryptographic algorithm
5. Format the encrypted result as a 20-digit token

### 2. Decoder Key Generation (`DKGA02.py`)

The DKGA02 (Decoder Key Generation Algorithm 02) implementation follows the STS specification for generating meter-specific decoder keys.

#### Key Functions:

- `DecoderKeyGenerator.generate_decoder_key()`: Generates a decoder key based on the meter number and other parameters.
- `read_vending_key()`: Reads the vending key from a file or generates a new one if it doesn't exist.
- `xor_bytes(a, b)`: Performs XOR operation on two byte arrays.

#### Algorithm Overview:

1. Read the vending key from `VendingKey.key` or generate a new one
2. Combine the key type, supply group code, tariff index, and key revision number
3. Apply cryptographic operations to generate a meter-specific decoder key
4. Output the decoder key in hexadecimal format

### 3. Token Decryption (`TokenDecrypter.py`)

The token decryption process simulates how a meter would decrypt a token to extract the purchased units.

#### Key Functions:

- `TokenDecrypter.decrypt_token(token_number)`: Decrypts a token and extracts its information.
- `_extract_token_bits(token_number)`: Converts the 20-digit token to its 66-bit binary representation.
- `_extract_class_bits(binary_token)`: Extracts and removes the class bits from the binary token.
- `_decrypt_block(encrypted_block)`: Decrypts the 64-bit encrypted block using the decoder key.
- `_parse_token_data(decrypted_block, class_bits)`: Parses the decrypted token data to extract fields.
- `_calculate_amount(amount_bits)`: Calculates the actual amount from the amount bits.

#### Algorithm Overview:

1. Extract the binary representation of the 20-digit token
2. Separate the class bits from the encrypted block
3. Decrypt the encrypted block using the decoder key
4. Parse the decrypted data to extract the token information
5. Calculate the actual units based on the token data

### 4. Data Cleaning (`data-cleaning.py`)

The data cleaning process extracts relevant information from raw token data.

#### Key Functions:

- `extract_token_info(file_path)`: Extracts token information from a text file.
- `clean_data(data)`: Cleans the extracted data.
- `save_to_csv(data, file_path)`: Saves the cleaned data to a CSV file.
- `save_to_excel(data, file_path)`: Saves the cleaned data to an Excel file.

#### Process Overview:

1. Read raw token data from `Raw-SMS-Meter-tokens.txt`
2. Extract meter number, token, amount, and other fields using regular expressions
3. Clean the data by converting to appropriate data types
4. Save the cleaned data to CSV and Excel files

### 5. Data Visualization (`TokenVisualizer.py`)

The data visualization component creates various charts and graphs to analyze token usage patterns.

#### Key Functions:

- `load_data(file_path)`: Loads token data from the cleaned CSV file.
- `plot_units_over_time(df)`: Plots the number of units purchased over time.
- `plot_amount_distribution(df)`: Plots a histogram of purchase amounts.
- `plot_units_per_amount(df)`: Plots a scatter plot showing units received per amount spent.
- `plot_monthly_spending(df)`: Plots the total monthly spending.
- `create_comprehensive_dashboard(df)`: Creates a comprehensive dashboard with multiple visualizations.
- `generate_summary_statistics(df)`: Generates and prints summary statistics for the token data.

#### Visualization Types:

1. **Units Over Time**: A line chart showing the number of units purchased over time.
2. **Amount Distribution**: A histogram showing the distribution of purchase amounts.
3. **Units per Amount**: A scatter plot with trend line showing the relationship between amount spent and units received.
4. **Monthly Spending**: A bar chart showing the total monthly spending.
5. **Comprehensive Dashboard**: A combined dashboard with multiple charts.

### 6. Testing Components (`test_components.py`)

The testing component verifies the functionality of the TokenDecrypter and TokenVisualizer components.

#### Key Functions:

- `test_token_decrypter()`: Tests the TokenDecrypter with a generated token.
- `test_token_visualizer()`: Tests the TokenVisualizer with the cleaned data.

#### Test Process:

1. Generate a token for a test meter number
2. Decrypt the token to verify correct extraction of units
3. Load the cleaned token data
4. Generate a test visualization
5. Report the test results

### 7. GUI Interface (`UtilityTokenGUI.py`)

The GUI interface provides a user-friendly way to interact with the project components.

#### Key Classes:

- `RedirectText`: Redirects stdout to a tkinter Text widget.
- `UtilityTokenApp`: Main application class for the Utility Token GUI.

#### Key Functions:

- `create_widgets()`: Creates and arranges all the widgets.
- `run_script(script_name, description)`: Runs a Python script and captures its output.
- Button command handlers for each component.

#### GUI Features:

1. Clean, modern interface with styled buttons
2. Output text area that displays command results
3. Status bar showing current operation
4. Separate thread execution to prevent UI freezing

## Data Flow

The typical data flow in the system is as follows:

1. **Token Generation**:
   - Input: Meter number, payment amount
   - Output: 20-digit token

2. **Token Decryption**:
   - Input: Meter number, token
   - Output: Decrypted token information including units

3. **Data Processing**:
   - Input: Raw token data from SMS messages
   - Output: Cleaned data in CSV and Excel formats

4. **Data Visualization**:
   - Input: Cleaned token data
   - Output: Various charts and graphs

## Security Considerations

While this project implements a simplified version of the STS, it includes several security features:

- **Meter-specific tokens**: Tokens are tied to specific meters and cannot be used on other meters.
- **Encryption**: Uses DES encryption for token security.
- **Decoder keys**: Generates unique decoder keys for each meter.
- **Vending key protection**: Stores the vending key securely.

## Performance Considerations

The project is designed for educational purposes and may not be optimized for high-performance production use. However, it includes several optimizations:

- **Caching**: The vending key is cached for reuse.
- **Efficient data structures**: Uses NumPy and Pandas for efficient data manipulation.
- **Parallel processing**: The GUI runs scripts in separate threads to prevent UI freezing.

## Future Enhancements

Potential future enhancements for the project include:

- **More accurate encryption**: Implement the exact EA07 process as outlined in the STS specifications.
- **Support for DKGA04 and EA11**: Add support for newer encryption algorithms.
- **Multiple utility types**: Extend the project to support water, gas, and other utilities.
- **Token lifecycle simulation**: Implement verification against duplicate tokens.

## References

- [Standard Transfer Specification (STS)](https://www.sts.org.za/)
- [Demystifying Utility Tokens - Part 1](https://mwangi-patrick.medium.com/lets-demystify-that-20-digit-utility-token-part-1-74c85eebbac4)
- [Demystifying Utility Tokens - Part 2](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-2-64ca45f4b88b)
- [Demystifying Utility Tokens - Part 3](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-3-d05002dbdf71)
- [Demystifying Utility Tokens - Part 4](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-4-9143c1c0792c)
