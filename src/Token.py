"""
 Simple script to generate a 20-digit numeric electricity token for demo purposes.
"""

import hashlib
import os

def generate_demo_token(meter_number: str, amount: float) -> str:
    """
    Simulates generation of a 20-digit numeric electricity token for demo purposes.

    Args:
        meter_number (str): The KPLC meter number (e.g., '37194275246')
        amount (float): The amount paid in KSh (minimum 5)

    Returns:
        str: A 20-digit numeric token
    """
    if amount < 5:
        raise ValueError("Amount must be at least KSh 5")

    seed = f"{meter_number}-{int(amount * 100)}-demo-key" # Unique seed for hashing
    hashed = hashlib.sha256(seed.encode()).hexdigest() # Hash the seed
    token = ''.join(filter(str.isdigit, hashed))[:20] # Extract digits and limit to 20 characters
    return format_token(token)

def format_token(token: str) -> str:
    """
    Format a 20-digit token with separators for better readability.
    
    Args:
        token (str): A 20-digit numeric token
    
    Returns:
        str: A formatted token with separators (e.g., 1234-5678-9012-3456-7890)
    """
    return '-'.join([token[i:i+4] for i in range(0, len(token), 4)])

def main():
    """Main function to run the token generator."""
    meter = input("Enter Meter Number: ")
    amount = float(input("Enter Amount (min KSh 5): "))

    try:
        token = generate_demo_token(meter, amount)
        print(f"\nGenerated Token: {token}")
    except ValueError as ve:
        print(f"Error: {ve}")

# Example usage
if __name__ == "__main__":
    main()
        
        
        
