import struct

LITTLE_ENDIAN = "<"
BIG_ENDIAN = ">"
FLOATS: str = "f"
INTS: str = "i"
SHORTS: str = "h"

def bytes_to_floats_le(binary: bytes) -> tuple[float,...]:
    num_of_floats: int = len(binary) // 4
    return struct.unpack(LITTLE_ENDIAN + str(num_of_floats) + FLOATS, binary)
def bytes_to_floats_be(binary: bytes, offset: int, len_bytes: int) -> tuple[float,...]:
    num_of_floats: int = len_bytes // 4
    return struct.unpack(BIG_ENDIAN + str(num_of_floats) + FLOATS, binary[offset: offset+len_bytes])

def bytes_to_float_le(binary: bytes, offset: int) -> int:
    return struct.unpack(LITTLE_ENDIAN + FLOATS, binary[offset:offset+4])[0]
def bytes_to_float_be(binary: bytes, offset: int) -> int:
    return struct.unpack(BIG_ENDIAN + FLOATS, binary[offset:offset+4])[0]

def bytes_to_int_le(binary: bytes, offset: int) -> int:
    return struct.unpack(LITTLE_ENDIAN + INTS, binary[offset:offset+4])[0]
def bytes_to_int_be(binary: bytes, offset: int) -> int:
    return struct.unpack(BIG_ENDIAN + INTS, binary[offset:offset+4])[0]


def bytes_to_short_le(binary: bytes, offset: int) -> int:
    return struct.unpack(LITTLE_ENDIAN + SHORTS, binary[offset:offset+2])[0]
def bytes_to_short_be(binary: bytes, offset: int) -> int:
    return struct.unpack(BIG_ENDIAN + SHORTS, binary[offset:offset+2])[0]