MOCCA+Peaksel integration
---

[MOCCA](https://github.com/Bayer-Group/MOCCA) is a library for advanced DAD/PDA data processing. Among others, it can deconvolute poorly resolves peaks using DAD spectra. But MOCCA can only work with text exports. So if you want to work with RAW HPLC data, it's possible to parse the native file using Peaksel, and then pass it to MOCCA.

First, install both packages:

```bash
pip install elsci-peaksel-sdk mocca2
```

# Deconvolve peaks using DAD

The following example fetches a previously uploaded injection ([here it is](https://peaksel.elsci.io/a/elsci/injection/8ehCvK0mufi)) by its ID:

```python
from matplotlib import pyplot as plt
from peakselsdk.Peaksel import Peaksel
from peakselsdk.dr.DetectorRun import DetectorType
from peakselsdk.integrations.mocca import to_mocca_chromatogram

# Fetch some injection from Peaksel:
peaksel = Peaksel("https://peaksel.elsci.io", org_name="elsci")
injection = peaksel.injections().get("8ehCvK0mufi")

# MOCCA can work only with DAD/PDA, so grabbing that:
uv_run = injection.detectorRuns.filter_by_type(DetectorType.UV)[0]

# Convert to MOCCA chromatogram:
chromatogram = to_mocca_chromatogram(peaksel, injection, uv_run)
# deconvolve peaks and plot
chromatogram.find_peaks(min_height=1)
chromatogram.deconvolve_peaks(model="FraserSuzuki", min_r2=0.99, relaxe_concs=False, max_comps=3)
chromatogram.plot()
plt.show()
```

If you want to upload raw data right in the same script, you need to create an account in Peaksel Hub or install Peaksel locally, and then it's just one additional line the script. See [the docs](../README.md).

# Batch-process many injections

Here we specify a small batch ([here it is](https://peaksel.elsci.io/a/elsci/batch/8eI9sHp8gqo)) with 5 injections, passing them all to MOCCA:

```python
from mocca2.dataset.dataset import MoccaDataset
from mocca2.dataset.settings import ProcessingSettings
from peakselsdk.Peaksel import Peaksel
from peakselsdk.dr.DetectorRun import DetectorType
from peakselsdk.injection.Injection import InjectionShort
from peakselsdk.integrations.mocca import to_mocca_chromatogram

peaksel = Peaksel("https://peaksel.elsci.io", org_name="elsci")
# Fetch all injections from the batch https://peaksel.elsci.io/a/elsci/batch/8eI9sHp8gqo
injections: [InjectionShort] = peaksel.batches().get_injections("8eI9sHp8gqo")

dataset = MoccaDataset()
for idx, j in enumerate(injections):
    print(f"Fetching injection {idx+1}/{len(injections)}")
    injection = peaksel.injections().get(j.eid)
    uv_run = injection.detectorRuns.filter_by_type(DetectorType.UV)[0]
    dataset.add_chromatogram(to_mocca_chromatogram(peaksel, injection, uv_run))

dataset.process_all(ProcessingSettings(), verbose=True, cores=1)
```

This doesn't do anything useful, in reality depending on what you want you'd need to specify Standards and visualize yields, etc. See more in [MOCCA batch-processing](https://bayer-group.github.io/MOCCA/ex_batch_processing.html). 