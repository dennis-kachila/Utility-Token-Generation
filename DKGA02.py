import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def generate_vending_key():
    """
    Generates an 8-byte DES vending key and writes it to 'VendingKey.key'
    in Base64 encoding.
    """
    key = get_random_bytes(8)  # DES key is 8 bytes
    with open("VendingKey.key", "w") as f:
        f.write(base64.b64encode(key).decode("utf-8"))
    return key

def read_vending_key():
    """
    Reads the vending key from the file 'VendingKey.key' and returns it as bytes.
    """
    with open("VendingKey.key", "r") as f:
        key_b64 = f.read().strip()
    return base64.b64decode(key_b64)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    """
    Returns the byte-wise XOR of two byte strings.
    """
    return bytes(x ^ y for x, y in zip(a, b))

class DecoderKeyGenerator:
    """
    Implements DKGA02 for decoder key generation.
    """
    IIN_1 = "0000"
    IIN_2 = "600727"
    
    def __init__(self, key_type, supply_group_code, tariff_index, key_revision_number, decoder_reference_number):
        self.key_type = key_type
        self.supply_group_code = supply_group_code
        self.tariff_index = tariff_index
        self.key_revision_number = key_revision_number
        self.decoder_reference_number = decoder_reference_number
        
        self.control_block = None  # Will hold a hex string (16 hex digits = 8 bytes)
        self.pan_block = None      # Hex string
        self.decoder_key_hex = None

    def build_control_block(self):
        """
        Builds the control block as a 16-digit hex string:
        key_type + supply_group_code + tariff_index + key_revision_number + "F" repeated 6 times.
        """
        # Build the string (as in Java: builder.append("F".repeat(6)))
        control_str = f"{self.key_type}{self.supply_group_code}{self.tariff_index}{self.key_revision_number}" + "F" * 6
        # Ensure the result is exactly 16 hex digits (8 bytes). If longer, slice; if shorter, pad.
        if len(control_str) > 16:
            control_str = control_str[:16]
        elif len(control_str) < 16:
            control_str = control_str.ljust(16, "F")
        self.control_block = control_str

    def build_pan_block(self):
        """
        Builds the PAN block as follows:
         - If the decoder reference number is 11 digits, use IIN_2 (dropping its first digit)
           otherwise use IIN_1, and then append the decoder reference number.
        """
        if len(self.decoder_reference_number) == 11:
            self.pan_block = self.IIN_2[1:] + self.decoder_reference_number
        else:
            self.pan_block = self.IIN_1 + self.decoder_reference_number

    def get_vending_key(self):
        """
        Reads and returns the vending key from the file.
        """
        return read_vending_key()

    def generate_decoder_key(self):
        """
        Generates the 64-bit decoder key following these steps:
          1. Build PAN and control blocks.
          2. XOR the PAN block and control block.
          3. DES encrypt the XOR result with the vending key.
          4. XOR the encrypted result with the XOR result.
          5. XOR the result with the vending key to produce the final decoder key.
        The final key is stored as an uppercase hex string in self.decoder_key_hex.
        """
        # Build the blocks
        self.build_pan_block()
        self.build_control_block()
        
        # Convert hex strings to bytes
        pan_block_bytes = bytes.fromhex(self.pan_block)
        control_block_bytes = bytes.fromhex(self.control_block)
        
        # Step 3: XOR PAN and control block bytes
        pan_control_xor = xor_bytes(pan_block_bytes, control_block_bytes)
        
        # Step 4: DES encrypt the XOR result using the vending key in ECB mode, NoPadding
        vending_key = self.get_vending_key()
        cipher = DES.new(vending_key, DES.MODE_ECB)
        encryption_result = cipher.encrypt(pan_control_xor)
        
        # Step 5: XOR the encrypted result with the XOR result from step 3
        encrypted_result_xor = xor_bytes(pan_control_xor, encryption_result)
        
        # Step 6: XOR the result with the vending key to obtain the decoder key
        decoder_key = xor_bytes(vending_key, encrypted_result_xor)
        self.decoder_key_hex = decoder_key.hex().upper()

    def get_decoder_key_hex(self):
        return self.decoder_key_hex

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    # Generate a vending key if not already present
    try:
        _ = read_vending_key()
    except Exception:
        generate_vending_key()
    
    # Example values (these are dummy values for illustration):
    # key_type = "2", supply_group_code = "123456", tariff_index = "7", key_revision_number = "1"
    # decoder_reference_number = "37194275246" (11 digits)
    dkg = DecoderKeyGenerator("2", "123456", "7", "1", "37194275246")
    dkg.generate_decoder_key()
    print("Decoder Key (Hex):", dkg.get_decoder_key_hex())
