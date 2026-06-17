# Unknown MS Peaks Analysis
---

`UnknownMsTotalPeakAnalysis` is a utility to automatically analyze "unknown" peaks of MS Total chromatograms.
It iterates over peaks that don't have an assigned analyte, extracts their spectra,
and allows you to provide a custom function to identify the substance.

## Example: Identify unknown peaks in a batch

The following example shows how to use `UnknownMsTotalPeakAnalysis` to process a whole batch of injections.
For each unknown peak found in MS detector runs, it calls a custom `spectrum_analyzer` function.
If the function identifies a substance (returns an `Analyte`), the peak is "identified" in Peaksel (linked to that analyte).

```python
from peakselsdk.Peaksel import Peaksel
from peakselsdk.blob.Spectrum import Spectrum
from peakselsdk.substance.Substance import Analyte, Substance
from peakselsdk.chromatogram.peak.Peak import UnknownPeak

# 1. Initialize Peaksel
# See README.md for more info on authentication
peaksel = Peaksel("https://peaksel.elsci.io", org_name="elsci")


# 2. Define your custom analyzer
def spectrum_analyzer(spectra: list[Spectrum], p:UnknownPeak, substances: list[Substance]) -> Analyte|Substance|None:
   """
   This function receives: 
    - All spectra **belonging to a peak**.
    - The unknown peak itself.
    - All substances that have been identified in the injection before running this script.
    
   You can use any logic here to identify the substance by analyzing the spectra.
   """
   # Example: calculate mean spectrum
   mean_spectrum = Spectrum.mean(spectra, bin_width=0.01)
   
   # Or skip the peak if its area is too small
   if p.area < 1000:
      return None

   # Or we're not interested in this rt range:
   if p.rt_minutes < 0.8 or 1.2 < p.rt_minutes:
      return None

   # Main logic to identify the substance...

   # Let's say we found it:
   return Analyte(
      alias="Caffeine",
      # Only one of these is required (mf or structure) 
      mf="C8H10N4O2",
      structure="CN1C=NC2=C1C(=O)N(C(=O)N2C)C",  # Caffeine SMILES  
   )
   # Or the spectrum matches to the one of existing substances:
   # return substance from 'substances'
   
   # Or if we didn't find anything:
   # return None


# 3. Run the analysis
analysis = peaksel.unknown_ms_total_peak_analysis(spectrum_analyzer)
# Optional: enable logging to see progress in console
analysis.logging_enabled(True)
# Process all injections in a specific batch
BATCH_ID = "your-batch-id"
analysis.analyze_batch(BATCH_ID)

# Or process a single injection
INJECTION_ID = "your-injection-id"
analysis.analyze_injection(INJECTION_ID)
```

## How it works

1. `analyze_batch(batch_id)` finds all injections in the batch that have unknown MS peaks on total chromatogram.
2. For each injection, it looks for MS Total chromatograms.
3. For each unknown peak in those chromatograms:
    - It fetches MS spectra within the peak's retention time range.
    - It calls your `analyzer` function with these spectra.
    - If your function returns an `Analyte`:
        - Adds this analyte to the injection (if it hasn't been yet added within this script execution).
        - Links the peak to this analyte.
