from collections import defaultdict

from peakselsdk.blob.blobs import bytes_to_short_be, bytes_to_int_be, bytes_to_float_be, bytes_to_floats_be


class BinaryHeader:
    """Binary data that consist of multiple fields are often transferred as a custom binary protocol. """

    HEADER_LEN_BYTES = 4
    FIELD_LEN_BYTES = 4

    def __init__(self, code: int, name: str, func_to_decode):
        self.code = code
        self.name = name
        self.decoder = func_to_decode

    def decode(self, binary: bytes, offset: int) -> any:
        return self.decoder(binary, offset)

    @staticmethod
    def from_bytes(binary: bytes, headers: tuple["BinaryHeader",...]) -> list["BinaryHeader"]:
        """
        :return: dict with `BinaryHeader.code -> index` in the object props
        """
        code_to_binheader: dict[int, BinaryHeader] = defaultdict(lambda: UNKNOWN_HEADER)
        for header in headers:
            code_to_binheader[header.code] = header
        result: list[BinaryHeader] = []
        if len(binary) < 4:
            return result
        offset: int = BinaryHeader.HEADER_LEN_BYTES
        header_end: int = offset + bytes_to_int_be(binary, 0)
        header_idx: int = 0
        while offset < header_end:
            header_code: int = bytes_to_short_be(binary, offset)
            result.append(code_to_binheader[header_code])
            offset += 2
            header_idx += 1
        return result

    def __str__(self)->str:
        return f"{self.name}({self.code})"

UNKNOWN_HEADER = BinaryHeader(-1, "Unknown", None)

def bin_to_float_converter(binary: bytes, offset: int):
    return bytes_to_float_be(binary, offset+4)
def bin_to_floats_converter(binary: bytes, offset: int):
    return bytes_to_floats_be(binary, offset+BinaryHeader.FIELD_LEN_BYTES, bytes_to_int_be(binary, offset))