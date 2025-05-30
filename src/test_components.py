"""
Test script to verify the functionality of TokenDecrypter.py and TokenVisualizer.py
"""

import os
import sys
import pandas as pd
from src.Token import generate_demo_token
from src.TokenDecrypter import TokenDecrypter
from src.TokenVisualizer import load_data, plot_units_over_time

def test_token_decrypter():
    """Test the TokenDecrypter with a generated token"""
    print("\n===== Testing TokenDecrypter =====")
    
    # Generate a token using the Token.py module
    meter_number = "37194275246"  # Example meter number
    amount = 100.0  # Example amount (KSh)
    
    print(f"Generating token for meter {meter_number} with amount KSh {amount}...")
    token = generate_demo_token(meter_number, amount)
    print(f"Generated token: {token}")
    
    # Decrypt the token
    print("\nDecrypting the token...")
    decrypter = TokenDecrypter(meter_number)
    try:
        result = decrypter.decrypt_token(token)
        print("\nDecrypted Token Information:")
        print(f"Token Class: {result['token_class']}")
        print(f"Subclass: {result['subclass']}")
        print(f"Random Number: {result['random_number']}")
        print(f"Token Identifier (TID): {result['tid']}")
        print(f"Calculated Units: {result['units']:.2f}")
        print("\nToken decryption test completed successfully!")
        return True
    except Exception as e:
        print(f"Error decrypting token: {e}")
        return False

def test_token_visualizer():
    """Test the TokenVisualizer with the cleaned data"""
    print("\n===== Testing TokenVisualizer =====")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_file = os.path.join(base_dir, "resources", "data", "cleaned_meter_data.csv")
    
    # Check if the cleaned data file exists
    if not os.path.exists(data_file):
        print(f"Data file '{data_file}' not found. Running data_cleaning.py first...")
        try:
            from src.data_cleaning import main as data_cleaning_main
            data_cleaning_main()
        except Exception as e:
            print(f"Error running data cleaning: {e}")
            return False
    
    if not os.path.exists(data_file):
        print(f"Error: Could not create or find data file '{data_file}'")
        return False
    
    # Load the data and generate a simple plot as a test
    try:
        print("Loading token data...")
        df = load_data()
        
        print("Generating a test visualization...")
        plot_units_over_time(df)
        
        print("\nTokenVisualizer test completed successfully!")
        return True
    except Exception as e:
        print(f"Error in TokenVisualizer: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Utility Token Generation Components ===\n")
    
    decrypter_result = test_token_decrypter()
    visualizer_result = test_token_visualizer()
    
    print("\n=== Test Summary ===")
    print(f"TokenDecrypter: {'PASSED' if decrypter_result else 'FAILED'}")
    print(f"TokenVisualizer: {'PASSED' if visualizer_result else 'FAILED'}")
    
    if decrypter_result and visualizer_result:
        print("\nAll tests passed successfully! The components are working correctly.")
    else:
        print("\nSome tests failed. Please check the error messages above.")

def main():
    """Main function to run the tests."""
    if __name__ == "__main__":
        print("=== Testing Utility Token Generation Components ===\n")
        
        decrypter_result = test_token_decrypter()
        visualizer_result = test_token_visualizer()
        
        print("\n=== Test Summary ===")
        print(f"TokenDecrypter: {'PASSED' if decrypter_result else 'FAILED'}")
        print(f"TokenVisualizer: {'PASSED' if visualizer_result else 'FAILED'}")
        
        if decrypter_result and visualizer_result:
            print("\nAll tests passed successfully! The components are working correctly.")
        else:
            print("\nSome tests failed. Please check the error messages above.")
