MOCCA integration
---

[MOCCA](https://github.com/Bayer-Group/MOCCA) is a library for advanced DAD/PDA data processing. Among others, it can deconvolute poorly resolves peaks using DAD spectra. But MOCCA can only work with text exports. So if you want to work with RAW HPLC data, it's possible to parse the native file using Peaksel, and then pass it to MOCCA.

First, install both Peaksel SDK and MOCCA:

```bash
pip install elsci-peaksel-sdk mocca2
```

This example fetches an already uploaded injection([here it is](https://peaksel.elsci.io/a/elsci/injection/8ehCv4tVR1U)) by its ID:

```python
from matplotlib import pyplot as plt
from peakselsdk.Peaksel import Peaksel
from peakselsdk.dr.DetectorRun import DetectorType
from peakselsdk.integrations.mocca import to_mocca_chromatogram

# Fetch some injection from Peaksel:
peaksel = Peaksel("https://peaksel.elsci.io", org_name="elsci")
injection = peaksel.injections().get("8ehCv4tVR1U")

# MOCCA can work only with DAD/PDA, so grabbing that:
uv_run = injection.detectorRuns.filter_by_type(DetectorType.UV)[0]

# Convert to MOCCA chromatogram and plot
chromatogram = to_mocca_chromatogram(peaksel, injection, uv_run)
chromatogram.plot()
plt.show()
```

If you want to upload raw data right in the same script, you need to create an account in Peaksel Hub or install Peaksel locally, and then it's just one additional line the script. See [the docs](../README.md).