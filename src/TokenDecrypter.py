"""
Token decryption module based on the STS (Standard Transfer Specification) standards.
This module implements the decryption process described in:
https://mwangi-patrick.medium.com/lets-demystify-that-20-digit-utility-token-part-3-d05002dbdf71
"""

import base64
import os
from Crypto.Cipher import DES
from src.DKGA02 import DecoderKeyGenerator, read_vending_key, xor_bytes

class TokenDecrypter:
    """
    Implements token decryption according to EA07 (Encryption Algorithm 7) of the STS.
    This simulates how a meter would decrypt a token to extract the information.
    """
    
    def __init__(self, meter_number, key_type="2", supply_group_code="123456", 
                 tariff_index="7", key_revision_number="1"):
        """
        Initialize the decrypter with the meter's information.
        
        Args:
            meter_number (str): The meter number (decoder reference number)
            key_type (str): The key type (default: "2")
            supply_group_code (str): The supply group code (default: "123456")
            tariff_index (str): The tariff index (default: "7")
            key_revision_number (str): The key revision number (default: "1")
        """
        self.meter_number = meter_number
        self.key_type = key_type
        self.supply_group_code = supply_group_code
        self.tariff_index = tariff_index
        self.key_revision_number = key_revision_number
        
        # Generate the decoder key for this meter
        self._generate_decoder_key()
    
    def _generate_decoder_key(self):
        """
        Generate the decoder key for this meter using DKGA02.
        """
        dkg = DecoderKeyGenerator(
            self.key_type, 
            self.supply_group_code, 
            self.tariff_index, 
            self.key_revision_number, 
            self.meter_number
        )
        dkg.generate_decoder_key()
        self.decoder_key_hex = dkg.get_decoder_key_hex()
        self.decoder_key = bytes.fromhex(self.decoder_key_hex)
    
    def _extract_token_bits(self, token_number):
        """
        Convert the 20-digit token to its 66-bit binary representation.
        
        Args:
            token_number (str): The 20-digit token number
        
        Returns:
            str: A 66-bit binary string
        """
        # Remove any separators from the token
        token_number = token_number.replace("-", "")
        
        # Convert to integer
        token_int = int(token_number)
        
        # Convert to binary (removing '0b' prefix) and ensure it's 66 bits
        binary = bin(token_int)[2:].zfill(66)
        
        return binary
    
    def _extract_class_bits(self, binary_token):
        """
        Extract and remove the class bits from the binary token.
        
        Args:
            binary_token (str): The 66-bit binary token
        
        Returns:
            tuple: (class_bits, 64-bit_encrypted_block)
        """
        # Extract the class bits (first 2 bits)
        class_bits = binary_token[:2]
        
        # The rest is the encrypted block
        encrypted_block = binary_token[2:]
        
        # Detranspose the class bits if needed (in a real implementation)
        # This would involve swapping with bits at positions 28 and 27
        
        return class_bits, encrypted_block
    
    def _decrypt_block(self, encrypted_block):
        """
        Decrypt the 64-bit encrypted block using the decoder key.
        
        Args:
            encrypted_block (str): The 64-bit encrypted binary block
        
        Returns:
            str: The decrypted binary block
        """
        # Convert binary string to bytes
        encrypted_bytes = int(encrypted_block, 2).to_bytes(8, byteorder='big')
        
        # In a real implementation, this would involve:
        # 1. Multiple rounds of inverse permutation
        # 2. Inverse substitution
        # 3. Key rotation
        # For simplicity, we'll use DES decryption as an approximation
        
        cipher = DES.new(self.decoder_key, DES.MODE_ECB)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        
        # Convert back to binary string
        decrypted_block = ''.join(format(byte, '08b') for byte in decrypted_bytes)
        
        return decrypted_block
    
    def _parse_token_data(self, decrypted_block, class_bits):
        """
        Parse the decrypted token data to extract fields.
        
        Args:
            decrypted_block (str): The decrypted 64-bit binary block
            class_bits (str): The 2-bit class identifier
        
        Returns:
            dict: A dictionary containing the token information
        """
        # In a real implementation, this would extract:
        # - Token class (from class_bits)
        # - Token subclass
        # - Random number
        # - Token identifier (TID)
        # - Amount
        # - CRC
        
        # For this demo, we'll just return a simple structure
        return {
            "token_class": int(class_bits, 2),
            "raw_decrypted_data": decrypted_block,
            # Additional parsing would be implemented here
            "subclass": int(decrypted_block[:4], 2),  # First 4 bits
            "random_number": int(decrypted_block[4:8], 2),  # Next 4 bits
            "tid": int(decrypted_block[8:32], 2),  # Next 24 bits
            "amount_bits": decrypted_block[32:48],  # Next 16 bits
            "crc": decrypted_block[48:]  # Last 16 bits
        }
    
    def _calculate_amount(self, amount_bits):
        """
        Calculate the actual amount from the amount bits.
        
        Args:
            amount_bits (str): The 16-bit amount field
        
        Returns:
            float: The calculated amount
        """
        # Extract exponent (first 2 bits)
        exponent_bits = amount_bits[:2]
        exponent = int(exponent_bits, 2)
        
        # Extract mantissa (remaining 14 bits)
        mantissa_bits = amount_bits[2:]
        mantissa = int(mantissa_bits, 2)
        
        # Calculate amount based on the formula
        if exponent == 0:
            amount = mantissa / 10.0
        else:
            amount = (10**exponent * mantissa + 2**14 * 10**(exponent-1)) / 10.0
        
        return amount
    
    def decrypt_token(self, token_number):
        """
        Decrypt a token and extract its information.
        
        Args:
            token_number (str): The 20-digit token number (with or without separators)
        
        Returns:
            dict: The extracted token information
        """
        # Extract token bits
        binary_token = self._extract_token_bits(token_number)
        
        # Extract class bits
        class_bits, encrypted_block = self._extract_class_bits(binary_token)
        
        # Decrypt the block
        decrypted_block = self._decrypt_block(encrypted_block)
        
        # Parse the decrypted data
        token_data = self._parse_token_data(decrypted_block, class_bits)
          # Calculate the actual units amount
        token_data["units"] = self._calculate_amount(token_data["amount_bits"])
        
        return token_data

def main():
    """Main function to run the token decrypter."""
    # Example token from the raw data file
    meter_number = input("Enter Meter Number (e.g., 37194275246): ")
    token = input("Enter Token (e.g., 1865-3776-4842-2132-9404): ")
    
    decrypter = TokenDecrypter(meter_number)
    
    try:
        result = decrypter.decrypt_token(token)
        print("\nDecrypted Token Information:")
        print(f"Token Class: {result['token_class']}")
        print(f"Subclass: {result['subclass']}")
        print(f"Random Number: {result['random_number']}")
        print(f"Token Identifier (TID): {result['tid']}")
        print(f"Calculated Units: {result['units']:.2f}")
    except Exception as e:
        print(f"Error decrypting token: {e}")

# Example usage
if __name__ == "__main__":
    main()
