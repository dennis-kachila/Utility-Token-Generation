"""
 Simple script to generate a 20-digit numeric electricity token for demo purposes.
"""


import hashlib

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
    print(seed)  # Debugging line to show the seed used for hashing
    hashed = hashlib.sha256(seed.encode()).hexdigest() # Hash the seed
    print(hashed)  # Debugging line to show the hashed value
    token = ''.join(filter(str.isdigit, hashed))[:20] # Extract digits and limit to 20 characters
    return token

# Example usage
if __name__ == "__main__":
    meter = input("Enter Meter Number: ")
    amount = float(input("Enter Amount (min KSh 5): "))

    try:
        token = generate_demo_token(meter, amount)
        print(f"\nGenerated Token: {token}")
    except ValueError as ve:
        print(f"Error: {ve}")
        
        
        
