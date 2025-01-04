import numpy as np
from mocca2 import Chromatogram
from mocca2.classes.data2d import Data2D
from peakselsdk.Peaksel import Peaksel
from peakselsdk.dr.DetectorRun import DetectorRun
from peakselsdk.injection.Injection import InjectionShort


def to_mocca_chromatogram(peaksel: Peaksel, injection: InjectionShort, uv_run: DetectorRun):
    if not uv_run.has_spectra():
        raise Exception(f"Only DAD/PDA can be converted to MOCCA Chromatogram, because it requires spectra. "
                        f"The DetectorRun({uv_run.detectorType}, {uv_run.eid}) that was passed has no spectra.")
    spectra = peaksel.blobs().get_spectra(uv_run.blobs.spectra)
    wl = np.array(spectra[0].x)
    time: list[float] = []
    data: list[tuple[float, ...]] = []
    for spectrum in spectra:
        data.append(spectrum.y)
        time.append(spectrum.rt)
    return Chromatogram(sample=Data2D(time=np.array(time), wavelength=wl, data=np.array(data).T), name=injection.name)