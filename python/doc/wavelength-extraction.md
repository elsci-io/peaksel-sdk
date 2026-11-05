Extracting a wavelength chromatogram in all injections of a batch
---

If a DAD/PDA records full spectra, Peaksel can extract any wavelength from them after the run. Peaksel saves the new chromatogram in each injection and detects its peaks. You need write access to the injections.

1. Extract the wavelength in all injections of the batch.
2. Fetch each injection, find the new chromatogram and analyze it with its peaks.

```python
from peakselsdk.Peaksel import Peaksel
from peakselsdk.chromatogram.Chrom import ExtractedWaveLength, WaveLength

# See README.md for more info on authentication
peaksel = Peaksel("https://peaksel.elsci.io", org_name="YOUR ORG", default_headers={"Cookie": "SESSION=YOUR SESSION ID"})
BATCH_ID = "your-batch-id"

# 1. Extract 254±4nm in all injections of the batch
wavelength = ExtractedWaveLength(WaveLength(254, 4))
peaksel.chroms().add_wavelength_to_batch(BATCH_ID, wavelength)

# 2. Analyze the new chromatograms
for inj in peaksel.injections().list_in_batch(BATCH_ID):
    injection = peaksel.injections().get(inj.eid)
    for chrom in injection.chromatograms.filter_by_wavelength(wavelength):
        peaks = injection.peaks.by_chromatogram(chrom.eid)  # peaks assigned to substances
        unknown_peaks = injection.unknown_peaks(chrom.eid)  # peaks not assigned to substances
        # The time axis is shared by all chromatograms of the detector run
        time = peaksel.blobs().get_detector_run_domain(chrom.domainId)
        signal = peaksel.blobs().get_chrom_signal(chrom.signalId)
        #
        #                     ==== YOUR CODE HERE ====
        #
        print(f"{injection.name} {chrom.name}: {len(peaks)} substance peaks, {len(unknown_peaks)} unknown peaks")
```

# Selected injections only

If you don't want the whole batch, give a list of injection IDs. Then analyze these injections the same way as in step 2:

```python
injection_ids = ["injection-id-1", "injection-id-2"]
peaksel.chroms().add_wavelength(injection_ids, wavelength)
for injection_id in injection_ids:
    injection = peaksel.injections().get(injection_id)
    for chrom in injection.chromatograms.filter_by_wavelength(wavelength):
        ...
```

# Reference wavelength

To subtract a reference wavelength, add it as the second `WaveLength`. This gives a chromatogram `254±4 - 360±50`:

```python
wavelength = ExtractedWaveLength(WaveLength(254, 4), WaveLength(360, 50))
peaksel.chroms().add_wavelength_to_batch(BATCH_ID, wavelength)
```

Before you use a reference wavelength, read about its problems in [DAD/PDA: Extracted and Reference wavelengths](https://elsci.io/docs/peaksel/wl-extraction.html).
