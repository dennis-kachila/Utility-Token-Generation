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

### 3. **Data Cleaning and Analysis**
   - Implemented in [`data-cleaning.py`](data-cleaning.py).
   - Processes raw token data from `Meter-tokens.txt` to extract and clean relevant fields.
   - Outputs cleaned data to `cleaned_meter_data.csv` and `cleaned_meter_data.xlsx` for further analysis.

---

## How to Use

### 1. **Generate a Demo Token**
   - Run [`Token.py`](Token.py) to generate a 20-digit token for a given meter number and payment amount:
     ```bash
     python Token.py
     ```
   - Enter the meter number and payment amount when prompted.

### 2. **Generate a Decoder Key**
   - Run  to generate a decoder key:
     ```bash
     python DKGA02.py
     ```
   - Example values for testing:
     - : "2"
     - : "123456"
     - : "7"
     - : "1"
     - : "37194275246"

### 3. **Clean and Analyze Token Data**
   - Run  to process raw token data:
     ```bash
     python data-cleaning.py
     ```
   - Outputs cleaned data to  and .

---

## Technical Details

### Encryption and Decryption
- Tokens are encrypted using the **DES (Data Encryption Standard)** algorithm.
- The encryption key (vending key) is an 8-byte key stored in .
- The decoder key is generated by combining the meter number and other parameters using the DKGA02 algorithm.

### Data Cleaning
- Raw token data is extracted from  using regular expressions.
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

- Implement token decryption to simulate the meter's behavior.
- Add support for other encryption algorithms (e.g., AES).
- Visualize token data using charts and graphs.
- Extend the project to support multiple utility types (e.g., water, gas).

---

## References

- [Standard Transfer Specification (STS)](https://www.sts.org.za/)
- [Demystifying Utility Tokens](https://mwangi-patrick.medium.com/lets-demystify-that-20-digit-utility-token-part-1-74c85eebbac4)

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.