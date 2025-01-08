Matchms + Peaksel integration
---

[matchms](https://matchms.readthedocs.io/) is a library for Mass Spec spectral processing e.g. spectral matching and searches. Combined with Peaksel, it's possible to parse vendor raw files, store them in the database, fetch the vendor-neutral data and feed it into matchms.

First, install both packages:

```bash
pip install elsci-peaksel-sdk matchms
```

The following example fetches a previously uploaded injection ([here it is](https://peaksel.elsci.io/a/elsci/injection/8fz92HY5CKW)) by its ID and creates matchms Spectrum objects:

```python
from peakselsdk.Peaksel import Peaksel
from peakselsdk.dr.DetectorRun import DetectorType
from peakselsdk.integrations.matchms import to_matchms_spectra


# Fetch some injection from Peaksel:
peaksel = Peaksel("https://peaksel.elsci.io", org_name="elsci")
injection = peaksel.injections().get("8fz92HY5CKW")

# Get the Product Ion Scan:
product_ion_scan_run = injection.detectorRuns.filter_by_type(DetectorType.QTOF_PROD_SCAN)[0]
# Fetch spectra and convert to matchms objects:
spectra = to_matchms_spectra(peaksel, product_ion_scan_run)
print(list(spectra))

```

Now you can do filtering and additional spectral processing and matching using the `spectra`.