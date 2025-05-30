# Utility Token Generation Project

## Overview

This project demonstrates the generation, processing, and analysis of prepaid utility tokens. Prepaid tokens are a modern solution for delivering credits for utility services such as electricity, water, or gas. They ensure financial safety for service providers by requiring customers to pay before accessing services, eliminating the need for manual meter readings or disconnection visits.

The tokens adhere to the **Standard Transfer Specification (STS)**, a global standard introduced in 1993 for secure transfer of utility credits. This project explores how these tokens are generated, how meters decrypt them, and why tokens are meter-specific.

---

## Key Concepts

### What is a Utility Token?

A utility token is typically a 20-digit numeric code in the format `0123–4567–8901–2345–6789`. These tokens are encrypted to securely store information such as the number of units purchased, the meter number, and other transaction details. The encryption ensures that only the intended meter can decrypt and use the token.

### How Does It Work?

1. **Payment and Token Generation**:
   - When a customer makes a payment, the utility provider calculates the number of units to allocate.
   - This information is encrypted using a **decoder key** unique to the customer's meter.
   - The encrypted data is sent to the customer as a 20-digit token.

2. **Token Decryption**:
   - The customer inputs the token into their meter.
   - The meter uses its stored decoder key to decrypt the token and extract the number of units purchased.

3. **Meter-Specific Tokens**:
   - Tokens are tied to specific meters because the encryption key used to generate the token corresponds to the decoder key stored in the meter.
   - This ensures that tokens cannot be used on unauthorized meters.

---

## Project Structure

The project consists of the following components:

### 1. **Token Generation**
   - Implemented in [`Token.py`](Token.py).
   - Simulates the generation of a 20-digit numeric token based on the meter number and payment amount.
   - Uses hashing to create a unique token for each transaction.

### 2. **Decoder Key Generation**
   - Implemented in [`DKGA02.py`](DKGA02.py).
   - Generates a **decoder key** using the DKGA02 algorithm.
   - The decoder key is used to encrypt and decrypt tokens securely.
   - Includes functionality for generating and reading a vending key stored in `VendingKey.key`.

### 3. **Token Decryption**
   - Implemented in [`TokenDecrypter.py`](TokenDecrypter.py).
   - Simulates how a meter would decrypt a token to extract the purchased units.
   - Uses the decoder key to reverse the encryption process.
   - Demonstrates the complete token lifecycle from generation to decryption.

### 4. **Data Cleaning and Analysis**
   - Implemented in [`data-cleaning.py`](data-cleaning.py).
   - Processes raw token data from `Raw-SMS-Meter-tokens.txt` to extract and clean relevant fields.
   - Outputs cleaned data to `cleaned_meter_data.csv` and `cleaned_meter_data.xlsx` for further analysis.

### 5. **Token Data Visualization**
   - Implemented in [`TokenVisualizer.py`](TokenVisualizer.py).
   - Creates various visualizations of token data, including usage patterns and spending analysis.
   - Generates charts for units purchased over time, amount distribution, and more.
   - Produces a comprehensive dashboard for data analysis.

### 6. **Testing Components**
   - Implemented in [`test_components.py`](test_components.py).
   - Provides automated tests for both the TokenDecrypter and TokenVisualizer.
   - Validates that token generation, decryption, and visualization work correctly.
   - Helps ensure the reliability of the components.

### 7. **GUI Interface**
   - Implemented in [`UtilityTokenGUI.py`](UtilityTokenGUI.py).
   - Provides a user-friendly graphical interface for all project components.
   - Allows users to generate tokens, decrypt tokens, and visualize data without using the command line.
   - Displays output in a scrollable text area for easy review.

---

## How to Use

### 1. **Generate a Demo Token**
   - Run [`Token.py`](Token.py) to generate a 20-digit token for a given meter number and payment amount:
     ```bash
     python Token.py
     ```
   - Enter the meter number and payment amount when prompted.

### 2. **Generate a Decoder Key**
   - Run [`DKGA02.py`](DKGA02.py) to generate a decoder key:
     ```bash
     python DKGA02.py
     ```
   - Example values for testing:
     - Key Type: "2"
     - Supply Group Code: "123456"
     - Tariff Index: "7"
     - Key Revision Number: "1"
     - Decoder Reference Number: "37194275246"

### 3. **Clean and Analyze Token Data**
   - Run [`data-cleaning.py`](data-cleaning.py) to process raw token data:
     ```bash
     python data-cleaning.py
     ```
   - Outputs cleaned data to `cleaned_meter_data.csv` and `cleaned_meter_data.xlsx`.

### 4. **Decrypt a Token**
   - Run [`TokenDecrypter.py`](TokenDecrypter.py) to simulate token decryption:
     ```bash
     python TokenDecrypter.py
     ```
   - Enter the meter number and token when prompted.

### 5. **Visualize Token Data**
   - Run [`TokenVisualizer.py`](TokenVisualizer.py) to generate visualizations of token usage:
     ```bash
     python TokenVisualizer.py
     ```
   - Creates multiple charts showing patterns and trends in token usage.

### 6. **Run Component Tests**
   - Run [`test_components.py`](test_components.py) to test the components:
     ```bash
     python test_components.py
     ```
   - This will verify that TokenDecrypter and TokenVisualizer are working correctly.

### 7. **Launch the GUI Interface**
   - Run [`UtilityTokenGUI.py`](UtilityTokenGUI.py) to launch the graphical interface:
     ```bash
     python UtilityTokenGUI.py
     ```
   - This provides a user-friendly way to access all project components.

### 8. **Using the Runner Scripts**
   - For convenience, you can use the runner scripts to access all components through a menu:
     - On Windows: `run.bat`
     - On Linux/macOS: `bash run.sh`

---

## Technical Details

### Encryption and Decryption
- Tokens are encrypted using the **DES (Data Encryption Standard)** algorithm.
- The encryption key (vending key) is an 8-byte key stored in `VendingKey.key`.
- The decoder key is generated by combining the meter number and other parameters using the DKGA02 algorithm.

### Data Cleaning
- Raw token data is extracted from `Raw-SMS-Meter-tokens.txt` using regular expressions.
- The cleaned data includes fields such as meter number, token, units, amount, and timestamp.

---

## Example Workflow

1. **Customer Payment**:
   - Customer pays KSh 100 for electricity.
   - The utility provider generates a token using the customer's meter number and payment amount.

2. **Token Input**:
   - Customer enters the token into their meter.
   - The meter decrypts the token using its decoder key and credits the purchased units.

3. **Data Analysis**:
   - The utility provider analyzes token data to track usage patterns and revenue.

---

## Future Enhancements

- Implement more accurate token encryption following the exact EA07 process as outlined in the STS specifications.
- Add support for DKGA04 and EA11 (MISTY1-based encryption) as described in part 4 of the reference article.
- Extend the project to support multiple utility types (e.g., water, gas).
- Implement a full simulation of the token lifecycle including verification against duplicate tokens.

---

## References

- [Standard Transfer Specification (STS)](https://www.sts.org.za/)
- [Demystifying Utility Tokens - Part 1](https://mwangi-patrick.medium.com/lets-demystify-that-20-digit-utility-token-part-1-74c85eebbac4)
- [Demystifying Utility Tokens - Part 2](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-2-64ca45f4b88b)
- [Demystifying Utility Tokens - Part 3](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-3-d05002dbdf71)
- [Demystifying Utility Tokens - Part 4](https://medium.com/codex/lets-demystify-that-20-digit-utility-token-part-4-9143c1c0792c)

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.