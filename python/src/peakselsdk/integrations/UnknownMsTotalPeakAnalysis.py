import logging
from logging import Logger
from typing import Callable

from peakselsdk.blob.BlobClient import BlobClient
from peakselsdk.blob.Spectrum import Spectrum
from peakselsdk.chromatogram.Chrom import Chrom
from peakselsdk.chromatogram.peak.Peak import UnknownPeak
from peakselsdk.substance.Substance import Substance
from peakselsdk.chromatogram.peak.PeakClient import PeakClient
from peakselsdk.dr.DetectorRun import AnalyticalMethod
from peakselsdk.injection.Injection import InjectionFull
from peakselsdk.injection.InjectionClient import InjectionClient
from peakselsdk.substance.SubstanceClient import SubstanceClient
from peakselsdk.substance.Substance import Analyte


class UnknownMsTotalPeakAnalysis:
    LOG: Logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")

    def __init__(self,
                 injections: InjectionClient,
                 substances: SubstanceClient,
                 blobs: BlobClient,
                 peaks: PeakClient,
                 analyzer: Callable[[list[Spectrum], UnknownPeak, list[Substance]], Analyte|Substance|None]):
        self._injections = injections
        self._substances = substances
        self._blobs = blobs
        self._peaks = peaks
        self._analyzer = analyzer
        self._logging_enabled = False
        self._progress_prefix = ""

    def analyze_batch(self, batch_id):
        injection_ids = self._injections.list_in_batch_with_unknown_ms_peaks(batch_id)
        total_injections = len(injection_ids)
        for i in range(0, total_injections):
            self._progress_prefix = f"[{i + 1}/{total_injections}]"
            self.analyze_injection(injection_ids[i])
        self._progress_prefix = ""

    def analyze_injection(self, injection_id):
        injection = self._injections.get(injection_id)
        created_analytes_cache = {}
        self._log(f"{self._progress_prefix} Analyzing injection {injection.name} ({injection_id})...")
        for ms_run in injection.detectorRuns.filter_by_analytical_method(AnalyticalMethod.MS):
            if not ms_run.blobs.spectra: continue
            chrom = injection.chromatograms.total(ms_run.eid)
            self.analyze_chromatogram(injection, chrom, created_analytes_cache)

    def analyze_chromatogram(self, injection: InjectionFull, chromatogram: Chrom, created_analytes_cache=None):
        if created_analytes_cache is None:
            created_analytes_cache = {}
        peaks = injection.unknown_peaks().by_chromatogram(chromatogram.eid)
        total_peaks = len(peaks)
        self._log(
            f"{self._progress_prefix} Chromatogram {chromatogram.name} ({chromatogram.eid}) contains {total_peaks} unknown peak(s).")
        for i in range(0, total_peaks):
            peak_progress = f"{self._progress_prefix} ({i+1}/{total_peaks})"
            peak = peaks[i]
            spectra = self._blobs.get_spectra_range(chromatogram.detectorId, peak.start_idx, peak.end_idx + 1)
            analyte = self._analyzer(spectra, peak, injection.substances)
            if analyte is None:
                self._log(f"{peak_progress} No analyte found for peak @rt={peak.rt_minutes}")
                continue
            substance_id = None
            if isinstance(analyte, Analyte):
                if analyte not in created_analytes_cache:
                    created_analytes_cache[analyte] = self._substances.add_analyte(injection.eid, analyte)
                substance_id = created_analytes_cache[analyte]
            elif isinstance(analyte, Substance):
                substance_id = analyte.eid
            self._log(
                f"{peak_progress} Peak @rt={peak.rt_minutes} matched to analyte ({analyte.alias or analyte.mf or analyte.structure})")
            self._peaks.add(injection.eid, chromatogram.eid, substance_id, peak.start_idx, peak.end_idx)

    def logging_enabled(self, enable: bool = True):
        self._logging_enabled = enable

    def _log(self, msg: str):
        if self._logging_enabled:
            UnknownMsTotalPeakAnalysis.LOG.info(msg)
