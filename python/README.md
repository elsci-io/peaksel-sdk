Peaksel SDK (Python)
---

A library to manage chromatography data in Peaksel: upload raw data, fetch the results of parsing (spectra, traces, peaks, injection info, etc).

Print some spectra info in console:

```python
from peakselsdk.Peaksel import Peaksel

org = "YOUR ORG NAME"  # or your username if you want to work with your personal data
auth_header = {"Cookie": "JSESSIONID=YOUR SESSION ID"}  # either cookie or Basic Auth
raw_data = "/path/to/zip/with/raw-data.zip"

base_url = "https://peaksel.elsci.io"
# The actual code to upload raw data, and retrieve all the parsed info:
peaksel = Peaksel(base_url, org_name=org, default_headers=auth_header)
injection_ids = peaksel.injections().upload(raw_data)  # upload your sample
j = peaksel.injections().get(injection_ids[0])  # fetch Injection info
for detectorRun in j.detectorRuns:
    spectra = peaksel.blobs().get_spectra(detectorRun.blobs.spectra)  # fetch spectra
    for spectrum in spectra:
        print(f"{spectrum.rt}: {spectrum.x}")
```

Before running this:
1. You need to [register at Peaksel Hub](https://peaksel.elsci.io), [get a private SaaS](https://elsci.io/peaksel/buy.html) or [install Peaksel](https://elsci.io/docs/peaksel/installation.html) on your machines.
2. Determine how you want to authenticate (service account or SessionID)

## Service Accounts auth (Basic Auth)

Service accounts can have their Basic Auth credentials specified in [Peaksel configs](https://elsci.io/docs/peaksel/security/users.html#inmemory-users). This option is available in Private SaaS and on-prem installations. For Peaksel Hub you need to request it explicitly (support@elsci.io). If this option is chosen, then in the code you set up auth headers this way:

```python
from peakselsdk.util.api_util import peaksel_basic_auth_header

auth_header = {"Authorization": peaksel_basic_auth_header("your username", "your password")}
```

## Session ID auth (Cookie)

If you're just playing, you can run the code on behalf of your own account. For this copy the cookie from your browser:

1. In Chrome: open Peaksel -> authenticate -> Press F12
2. Go to Application tab -> Cookies -> click on the website URL -> copy the Value of the JSESSIONID cookie

Now in the code you set up Peaksel this way:

```python
auth_header = {"Cookie": "JSESSIONID=YOUR SESSION ID"}
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

1. Install [uv](https://github.com/astral-sh/uv) build tool and run `uv build`
2. In PyCharm mark `src` as Sources Root and `test` as Test Sources Root
3. To run the tests `./test.sh`