from enum import Enum

from peakselsdk.blob.BinaryProtocol import BinaryHeader, bin_to_float_converter, bin_to_floats_converter
from peakselsdk.blob.blobs import bytes_to_int_be


class SpectrumProp(Enum):
    RT = BinaryHeader(1, "Retention Time", bin_to_float_converter)
    TOTAL_SIGNAL = BinaryHeader(2, "Total Signal", bin_to_float_converter)
    BASE = BinaryHeader(3, "Base", bin_to_float_converter)
    PRECURSOR_ION = BinaryHeader(4, "Precursor Ion", bin_to_float_converter)
    SRM_PRODUCTS = BinaryHeader(5, "SRM Product Ions", bin_to_floats_converter)
    X = BinaryHeader(6, "x", bin_to_floats_converter)
    Y = BinaryHeader(7, "x", bin_to_floats_converter)

    @staticmethod
    def values() -> tuple[BinaryHeader,...]:
        return tuple([e.value for e in SpectrumProp])

class Spectrum:
    def __init__(self, props: dict[int, any]):
        self.props: dict[int, any] = props

    @staticmethod
    def from_bytes(binary: bytes) -> list["Spectrum"]:
        """
        The binary object format starts with the list of headers (and defines their order in each spectrum),
        followed by the actual spectra:
        header: [header len (i4)] [header1_code (i2),...]
        spectra: [spectrum_total_len (i4) {spectrum1_len (i4), {prop1_len (i4), prop1_val, ...}, ...]
        """
        return _bytes_to_spectrum(binary)

    @property
    def x(self) -> tuple[float,...]:
        return self.get_prop(SpectrumProp.X)
    @property
    def y(self) -> tuple[float, ...]:
        return self.get_prop(SpectrumProp.Y)
    @property
    def rt(self) -> float:
        return self.get_prop(SpectrumProp.RT)
    @property
    def total_signal(self) -> float:
        return self.get_prop(SpectrumProp.TOTAL_SIGNAL)
    @property
    def base(self) -> float:
        return self.get_prop(SpectrumProp.BASE)

    def has_prop(self, header: SpectrumProp) -> bool:
        return header.value.code in self.props

    def get_prop(self, header: SpectrumProp) -> any:
        if header.value.code in self.props:
            return self.props[header.value.code]
        raise Exception(f"Property {header.name} doesn't exist in this Spectrum")

def _bytes_to_spectrum(binary: bytes) -> list["Spectrum"]: # moved the body of hte method so that the class looks clearer
    if len(binary) == 0:
        return []
    result: list[Spectrum] = []
    headers: list[BinaryHeader] = BinaryHeader.from_bytes(binary, SpectrumProp.values())

    SPECTRUM_LEN_BYTES = 4 # before each spectrum there's an int with the byte length of the spectrum
    PROP_LEN_BYTES = 4 # before each property there's an int with the byte length of the value

    current_offset: int = bytes_to_int_be(binary, 0) + BinaryHeader.HEADER_LEN_BYTES
    while current_offset < len(binary):
        current_offset += SPECTRUM_LEN_BYTES
        spectrum_props: dict[int, any] = {}
        rt: float
        for header in headers:
            prop_len: int = bytes_to_int_be(binary, current_offset)
            if header.decoder is not None:
                prop_val = header.decode(binary, current_offset)
                spectrum_props[header.code] = prop_val
            current_offset = current_offset + PROP_LEN_BYTES + prop_len
        result.append(Spectrum(spectrum_props))
    return result

