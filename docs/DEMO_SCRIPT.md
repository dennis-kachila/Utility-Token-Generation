# Utility Token Generation - Demo Video Script

## Introduction (0:00 - 0:30)

[Opening slide with project title]

**Narrator:** Welcome to this demonstration of the Utility Token Generation project. This project demonstrates how prepaid utility tokens work, from generation to decryption and analysis. We'll explore the Standard Transfer Specification (STS) that ensures secure transfer of utility credits.

## Project Overview (0:30 - 1:30)

[Show slide with project components]

**Narrator:** The project consists of several components:
1. Token Generation - for creating new tokens
2. Decoder Key Generation - for creating meter-specific keys
3. Token Decryption - for extracting the purchased units
4. Data Cleaning - for processing raw token data
5. Data Visualization - for analyzing token usage patterns
6. GUI Interface - for easy interaction with all components

Let's see how each of these works in practice.

## Setting Up (1:30 - 2:00)

[Show terminal with setup commands]

**Narrator:** Before we start, let's make sure our environment is set up correctly. We'll use a virtual environment and install the required dependencies.

```bash
# Create and activate virtual environment
python -m venv utility
source utility/bin/activate  # On Windows: utility\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Token Generation Demo (2:00 - 3:30)

[Show running Token.py]

**Narrator:** Let's start by generating a token. When a customer makes a payment, the utility provider needs to generate a token that contains information about the purchased units.

```bash
python Token.py
```

**Narrator:** We'll enter a meter number - let's use 37194275246, and an amount - let's say 100 Kenyan Shillings.

[Show output of token generation]

**Narrator:** As you can see, the system has generated a 20-digit token. This token is encrypted and can only be used with the specific meter it was generated for.

## Decoder Key Generation Demo (3:30 - 4:30)

[Show running DKGA02.py]

**Narrator:** Now, let's see how decoder keys are generated. Each meter has a unique decoder key that's used to encrypt and decrypt tokens.

```bash
python DKGA02.py
```

**Narrator:** We'll enter the same meter information to generate a decoder key.

[Show output of key generation]

**Narrator:** The decoder key is a 64-bit hexadecimal value that would be stored in the meter during manufacturing.

## Token Decryption Demo (4:30 - 5:30)

[Show running TokenDecrypter.py]

**Narrator:** When a customer receives a token, they enter it into their meter. The meter uses its decoder key to decrypt the token and extract the purchased units.

```bash
python TokenDecrypter.py
```

**Narrator:** We'll enter the meter number and the token we generated earlier.

[Show output of token decryption]

**Narrator:** The decryption process has successfully extracted the token information, including the number of units purchased.

## Data Cleaning Demo (5:30 - 6:30)

[Show running data-cleaning.py]

**Narrator:** Utility providers often receive token data in a raw format. Let's see how we can clean and process this data.

```bash
python data-cleaning.py
```

[Show output of data cleaning]

**Narrator:** The system has processed the raw token data from the input file and generated cleaned CSV and Excel files for further analysis.

## Data Visualization Demo (6:30 - 8:00)

[Show running TokenVisualizer.py]

**Narrator:** Now, let's visualize the token data to understand usage patterns.

```bash
python TokenVisualizer.py
```

[Show output of visualizations]

**Narrator:** The system has generated several visualizations:
1. Units purchased over time
2. Distribution of purchase amounts
3. Units received per amount spent
4. Monthly spending patterns
5. A comprehensive dashboard

These visualizations help utility providers and customers understand usage patterns and make informed decisions.

## GUI Interface Demo (8:00 - 9:30)

[Show launching UtilityTokenGUI.py]

**Narrator:** For a more user-friendly experience, the project includes a graphical interface.

```bash
python UtilityTokenGUI.py
```

[Show GUI interface]

**Narrator:** The GUI provides easy access to all the project components. Let's try generating a token using the GUI.

[Demonstrate using the GUI to generate a token]

**Narrator:** We can also decrypt tokens, process data, and generate visualizations using the GUI.

## Running Tests (9:30 - 10:00)

[Show running test_components.py]

**Narrator:** To ensure that all components are working correctly, the project includes a test script.

```bash
python test_components.py
```

[Show output of tests]

**Narrator:** All tests have passed, indicating that the components are functioning as expected.

## Using the Runner Scripts (10:00 - 10:30)

[Show running run.sh or run.bat]

**Narrator:** For convenience, the project includes runner scripts that provide a menu-based interface.

```bash
bash run.sh  # On Windows: run.bat
```

[Show menu interface]

**Narrator:** We can select any of the components from this menu.

## Conclusion (10:30 - 11:00)

[Show closing slide with project information]

**Narrator:** That concludes our demonstration of the Utility Token Generation project. This project provides a comprehensive simulation of how prepaid utility tokens work, from generation to analysis.

The code is available on GitHub, and the project is open source. Feel free to explore, modify, and extend it for your own purposes.

Thank you for watching!
