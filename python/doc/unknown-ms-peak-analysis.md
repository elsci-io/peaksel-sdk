Identifying Unknown MS Peaks on Total Chromatograms in a batch
---

The following example shows how to process a whole batch of injections.
For each unknown peak found in MS detector runs, we can perform some inspection (area, RT, m/z) 
and then use its spectrum to identify the substance.
If a substance is identified (e.g. `SubstanceChem`), the peak can be linked to that analyte in Peaksel.

```python
from collections import defaultdict
from peakselsdk.Peaksel import Peaksel
from peakselsdk.blob.Spectrum import Spectrum
from peakselsdk.chromatogram.Chrom import Chrom
from peakselsdk.substance.Substance import SubstanceChem
from peakselsdk.chromatogram.peak.Peak import UnknownPeak

# 1. Initialize Peaksel
# See README.md for more info on authentication
peaksel = Peaksel("https://peaksel.elsci.io", org_name="elsci")
BATCH_ID = "your-batch-id"

# 2. Iterate over injections with unknown MS peaks on Total chromatograms
#    and process each unknown peak to identify the analyte
injection_ids = peaksel.injections().list_in_batch_with_unknown_ms_peaks(BATCH_ID)
for injection_id in injection_ids:
    injection = peaksel.injections().get(injection_id)
    # Here we will store the found analytes
    found_analytes: dict[SubstanceChem, list[tuple[Chrom, UnknownPeak]]] = defaultdict(list)
    # Iterate over MS detector runs and inspect peaks of TIC chromatogram
    for ms_run in injection.detectorRuns.filter_by_analytical_method("MS"):
        chrom = injection.chromatograms.get_total(ms_run.eid)
        unknown_peaks = injection.unknown_peaks(chrom.eid)
        if not unknown_peaks or not ms_run.blobs.spectra: continue
        spectra = peaksel.blobs().get_spectra(ms_run.blobs.spectra)
        for peak in unknown_peaks:
            # 1. PEAK INSPECTION
            # Example: Check if the peak meets criteria to be analyte
            if peak.area < 1000: continue # Peak area is too small to be an analyte
            if peak.rt_minutes < 0.8 or 1.2 < peak.rt_minutes: continue # Peak is too far from the expected retention time
            if peak.base < 298.0 or 300.0 < peak.base: continue # Most abundant m/z (at peak's RT) is too low or high
            # 2. SPECTRUM CALCULATION AND INSPECTION
            # Example: calculate the mean spectrum of the peak
            mean_spectrum = Spectrum.mean(spectra, start_idx=peak.start_idx, end_idx=peak.end_idx + 1,
                                          bin_width=0.00001)
            # Do some black magic with the spectrum to find the analyte
            # ==== YOUR CODE HERE ====
            # Once you have the analyte, you can add it to the list of found analytes
            # Example: add Glucose to the list of found analytes
            analyte = SubstanceChem(mf='C6H12O6', alias='Glucose')
            # Track the chromatogram and peak for the analyte, so we can link them later
            found_analytes[analyte].append((chrom, peak))
    # Let's iterate over the found analytes and process them
    for analyte in found_analytes:
        # Is the analyte already in the list of substances?
        existing_analyte = next((s for s in injection.substances if s.mf == analyte.mf or s.alias == analyte.alias), None)
        if not existing_analyte:
            # If not, add it to the list of substances.
            # This will also create XIC for the analyte and detect peaks automatically. 
            peaksel.substances().add(injection_id, analyte)
        else:
            # Such analyte already exists, we can add its peaks to the injection.
            analyzed_peaks = found_analytes[analyte]
            for chrom, peak in analyzed_peaks:
                peaksel.peaks().add(injection_id, chrom.eid, existing_analyte.eid, peak.start_idx, peak.end_idx)
```