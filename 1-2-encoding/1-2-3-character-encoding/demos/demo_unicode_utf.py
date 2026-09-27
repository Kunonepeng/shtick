"""Q10-Q11 fallback demo for v6-2. No third-party packages required."""

SAMPLES = [
    ("A", "A"),
    ("中", "中"),
    ("你", "你"),
    ("U+1F600", chr(0x1F600)),
]

def hex_bytes(text, encoding):
    return text.encode(encoding).hex(" ").upper()

def utf16be_units(text):
    raw = text.encode("utf-16-be")
    return [raw[i:i+2].hex().upper() for i in range(0, len(raw), 2)]

def utf32be_units(text):
    raw = text.encode("utf-32-be")
    return [raw[i:i+4].hex().upper() for i in range(0, len(raw), 4)]

print("=== Unicode character identity ===")
for label, ch in SAMPLES:
    print(f"{label:<10} -> U+{ord(ch):04X}")

print("\n=== Same code point, different UTF bytes ===")
for label, ch in SAMPLES:
    print(f"\n{label}  U+{ord(ch):04X}")
    print("  UTF-8    :", hex_bytes(ch, "utf-8"))
    print("  UTF-16BE :", hex_bytes(ch, "utf-16-be"))
    print("  UTF-32BE :", hex_bytes(ch, "utf-32-be"))

print("\n=== Code-unit view ===")
print("UTF-8   : 8-bit code units")
print("UTF-16  : 16-bit code units")
print("UTF-32  : 32-bit code units")
print()
print(f"{'sample':<10} {'code point':<11} {'UTF-8 units':<18} {'UTF-16 units':<18} {'UTF-32 units'}")
print("-" * 88)
for label, ch in SAMPLES:
    u8 = [f"{b:02X}" for b in ch.encode("utf-8")]
    u16 = utf16be_units(ch)
    u32 = utf32be_units(ch)
    print(f"{label:<10} U+{ord(ch):04X}      {' '.join(u8):<18} {' '.join(u16):<18} {' '.join(u32)}")

print("\nKey observation:")
print("- U+1F600 uses TWO 16-bit UTF-16 code units: D83D DE00.")
print("- Therefore UTF-16 does not mean 'every character is 16 bits'.")
