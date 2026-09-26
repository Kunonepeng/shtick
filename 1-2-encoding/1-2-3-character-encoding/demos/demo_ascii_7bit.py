"""Q3: Show why ASCII is a 7-bit code but is commonly stored in one byte."""

ch = "A"
code = ord(ch)
ascii_byte = ch.encode("ascii")[0]

print(f"Character        : {ch}")
print(f"Decimal code     : {code}")
print(f"Hex code         : 0x{code:02X}")
print(f"ASCII 7-bit code : {code:07b}")
print(f"Stored in 1 byte : {ascii_byte:08b}")
print(f"MSB              : {(ascii_byte >> 7) & 1}")
