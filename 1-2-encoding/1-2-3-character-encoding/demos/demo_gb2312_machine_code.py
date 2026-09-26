"""Q6-Q7 Plan B: inspect GB2312 bytes without WinHex.

The demo intentionally uses characters inside GB2312 so students can observe the
traditional textbook model:
- ASCII characters use one byte whose MSB is 0.
- GB2312 Chinese characters use two bytes; both bytes have MSB 1.
"""

TEXT = "A中B国C文"


def bits(byte: int) -> str:
    return f"{byte:08b}"


def msb(byte: int) -> int:
    return (byte >> 7) & 1


def inspect_character(ch: str) -> None:
    raw = ch.encode("gb2312")
    hex_bytes = " ".join(f"{b:02X}" for b in raw)
    binary = " ".join(bits(b) for b in raw)
    msbs = " ".join(str(msb(b)) for b in raw)

    print(
        f"{ch:<2} | {hex_bytes:<7} | {len(raw)} byte(s) | "
        f"{binary:<17} | MSB: {msbs}"
    )


print("Text:", TEXT)
raw = TEXT.encode("gb2312")
print("GB2312 bytes:", raw.hex(" ").upper())
print()
print("字符 | Hex     | 长度      | Binary            | MSB")
print("-" * 64)

for ch in TEXT:
    inspect_character(ch)

print("\n结论（仅针对本实验中的 GB2312 机内码模型）：")
print("- ASCII: 1 byte, MSB = 0")
print("- 汉字  : 2 bytes, both MSBs = 1")
