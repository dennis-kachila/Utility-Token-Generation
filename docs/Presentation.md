```
# Utility Token Generation
## Understanding the Standard Transfer Specification (STS)
---

## What is a Utility Token?

- A 20-digit numeric code (e.g., `0123-4567-8901-2345-6789`)
- Used for prepaid utility services (electricity, water, gas)
- Encrypted to ensure security and prevent unauthorized use
- Contains information about units purchased, meter ID, etc.

---

## How Do Utility Tokens Work?

1. **Customer makes a payment** for utility credits
2. **Payment system generates a token** specific to the customer's meter
3. **Customer enters token** into their meter
4. **Meter decrypts the token** and credits the purchased units

---

## Technical Implementation

### Encryption & Decryption
- Based on the Standard Transfer Specification (STS)
- Uses DKGA02 algorithm for decoder key generation
- Implements EA07 encryption algorithm

### Key Components
- **Vending Key**: Master key for the utility provider
- **Decoder Key**: Meter-specific key derived from the vending key
- **Token**: Encrypted data package with purchase information

---

## Project Components

1. **Token Generation** (`Token.py`)
2. **Decoder Key Generation** (`DKGA02.py`)
3. **Token Decryption** (`TokenDecrypter.py`)
4. **Data Cleaning** (`data-cleaning.py`)
5. **Data Visualization** (`TokenVisualizer.py`)
6. **Component Testing** (`test_components.py`)
7. **GUI Interface** (`UtilityTokenGUI.py`)

---

## Token Generation Process

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Vending Key  │────>│  Decoder Key  │────>│     Token     │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Master Key   │     │ Meter-specific│     │Encrypted credit│
│  (Provider)   │     │     key       │     │   information  │
└───────────────┘     └───────────────┘     └───────────────┘
```

---

## Token Decryption Process

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│     Token     │────>│  Decoder Key  │────>│  Credit Units │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ 20-digit code │     │ Stored in the │     │ Credited to   │
│ entered by user│     │    meter      │     │customer account│
└───────────────┘     └───────────────┘     └───────────────┘
```

---

## Data Visualization

- **Units Over Time**: Track consumption patterns
- **Amount Distribution**: Analyze spending habits
- **Units per Amount**: Monitor utility pricing
- **Monthly Spending**: Track financial trends
- **Comprehensive Dashboard**: Combined analytics

---

## Demo & Resources

### Quick Demo
- Generate a token for meter 37194275246
- Decrypt the token to extract the units
- Analyze token data through visualizations

### Resources
- [Project Repository](https://github.com/yourusername/utility-token-generation)
- [STS Official Website](https://www.sts.org.za/)
- [Medium Article Series on Utility Tokens](https://mwangi-patrick.medium.com/lets-demystify-that-20-digit-utility-token-part-1-74c85eebbac4)

---

## Thank You!

**Questions?**
```
