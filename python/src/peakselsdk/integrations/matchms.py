from typing import Iterable
import numpy as np

from matchms.Spectrum import Spectrum
from peakselsdk.Peaksel import Peaksel
from peakselsdk.blob.Spectrum import SpectrumProp
from peakselsdk.dr.DetectorRun import DetectorRun
from peakselsdk.dr.DetectorRun import AnalyticalMethod

def to_matchms_spectra(peaksel: Peaksel, ms_run: DetectorRun) -> Iterable[Spectrum]:
    if ms_run.analyticalMethod != AnalyticalMethod.MS:
        raise Exception(f"The DetectorRun({ms_run.detectorType}, {ms_run.eid}) is not Mass Spec")
    if not ms_run.has_spectra():
        raise Exception(f"Only Mass Spec runs with spectra can be converted to MatchMS Spectrum list. "
                        f"The DetectorRun({ms_run.detectorType}, {ms_run.eid}) that was passed has no spectra.")
    spectra = peaksel.blobs().get_spectra(ms_run.blobs.spectra)
    ion_mode = "positive" if ms_run.is_positive_ion_mode() else "negative"
    for peaksel_spectrum in spectra:
        props = {
            "retention_time": peaksel_spectrum.rt,
            "ionmode": ion_mode
        }
        if peaksel_spectrum.has_prop(SpectrumProp.PRECURSOR_ION):
            props["precursor_mz"] = peaksel_spectrum.get_prop(SpectrumProp.PRECURSOR_ION)
        yield Spectrum(np.array(peaksel_spectrum.x), np.array(peaksel_spectrum.y), metadata=props)