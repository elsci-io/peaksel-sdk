Peaksel SDK (Python)
---

A library to manage chromatography data in [Peaksel](https://elsci.io/peaksel/): upload raw data, fetch the results of parsing (spectra, traces, peaks, injection info, etc). 

If you need some advanced processing (like peak deconvolution), you can combine it with:

- [MOCCA](./doc/mocca-integration.md) for DAD/PDA spectral processing for peak deconvolution, purity and yield calculations
- [matchms](doc/matchms-integration.md) for Mass Spec (especially Tandem MS) spectral processing, as well as isotopic pattern score matching and searching, and other machine learning capabilities.

To install Peaksel SDK:

```bash
pip install elsci-peaksel-sdk
```

# Examples

## Read public data

First, we're going to read an already uploaded injection (like [this one](https://peaksel.elsci.io/a/elsci/injection/8ehCv4tVR1U)), and print some spectra info from each detector:

```python
from peakselsdk.Peaksel import Peaksel

# Initialize the entry point:
peaksel = Peaksel("https://peaksel.elsci.io", org_name="elsci")

# Fetch injection info:
injection = peaksel.injections().get("8ehCv4tVR1U")

# Go through all detectors and print the spectra:
for detectorRun in injection.detectorRuns:
    if not detectorRun.has_spectra():
        continue
    spectra = peaksel.blobs().get_spectra(detectorRun.blobs.spectra)  # fetch spectra
    for spectrum in spectra:
        print(f"{spectrum.rt}: {spectrum.x}")
```

## Uploading & parsing vendor files

If you want to upload an injection or read private data, you must authenticate. The general steps stay similar though:

```python
from peakselsdk.Peaksel import Peaksel

org = "YOUR ORG NAME"  # or your username if you want to work with your personal data
auth_header = {"Cookie": "SESSION=YOUR SESSION ID"}  # either cookie or Basic Auth
raw_data = "/path/to/zip/with/raw-data.zip"

# Entry point to Peaksel:
peaksel = Peaksel("https://peaksel.elsci.io", org_name=org, default_headers=auth_header)

# Upload & parse, get the ID back:
injection_ids = peaksel.injections().upload(raw_data) 

# Fetch injection info:
injection = peaksel.injections().get(injection_ids[0])

# Now you can do the same operations as in the previous example
# ...
```

Before running this:
1. You need to [register at Peaksel Hub](https://peaksel.elsci.io), [get a private SaaS](https://elsci.io/peaksel/buy.html) or [install Peaksel](https://elsci.io/docs/peaksel/installation.html) on your machines.
2. Determine how you want to authenticate (service account or SessionID, see the next section)

# Authentication

## Session ID auth (Cookie)

If you're just playing, you can run the code on behalf of your own account:

```python
auth_header = {"Cookie": "SESSION=YOUR SESSION ID"}
```

You can get this cookie from the browser:

1. In Chrome: open Peaksel -> authenticate -> Press F12
2. Go to Application tab -> Cookies -> click on the website URL -> copy the Value of the JSESSIONID cookie


## Service Accounts auth (Basic Auth)

Service accounts can have their Basic Auth credentials specified in [Peaksel configs](https://elsci.io/docs/peaksel/security/users.html#inmemory-users). This option is available in Private SaaS and on-prem installations. For Peaksel Hub you need to request it (support@elsci.io). If you go with Basic Auth, then in the code you set up auth headers this way:

```python
from peakselsdk.util.api_util import peaksel_basic_auth_header

auth_header = {"Authorization": peaksel_basic_auth_header("your username", "your password")}
```

# Design & Conventions

All the necessary functionality is exposed from `peakselsdk.Peaksel` class - just use its methods to work with Injections, Batches, Substances (analytes), Peaks, etc.

* `XxxClient` are classes to communicate with the app API, they are created and returned by `Peaksel` entrypoint
* Classes like `User`, `Org`, `Injection` capture the actual requests and responses
   * Fields are `camelCased` to match the JSON structure
   * The JSON's `id` is actually stored in `eid` (aka entity id) in the classes. Because `id` has special meaning in Python.  
   * Every `__init__()` has `**kwargs` param that is ignored. This is needed to simplify parsing of response JSONs, 
     as we always keep the names in the classes and JSONs the same, so when passing those as dict into the constructor,
     the corresponding fields are set. But it's possible that in Peaksel we add a new param, and this would break 
     dict->DTO conversion as the param will be unknown. So to be forward-compatible, we add `**kwargs` to capture 
     all the unknown fields.

# Working with source code

1. Install [uv](https://github.com/astral-sh/uv) build tool and run: `uv venv && uv sync && uv build`
2. In PyCharm mark `src` as Sources Root and `test` as Test Sources Root
3. To run the tests `./test.sh`