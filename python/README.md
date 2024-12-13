Peaksel SDK (Python)
---

# Architecture & Conventions

* `Peaksel` class is an entrypoint to all the clients
* `XxxClient` are classes to communicate with the app API
* Classes like `User`, `Org`, `Injection` capture the actual requests and responses
   * The JSON's `id` is actually stored in `eid` (aka entity id) in the classes. Because `id` has special meaning in Python.  
   * Every `__init__()` has `**kwargs` param that is ignored. This is needed to simplify parsing of response JSONs, as we always keep the names in the classes and JSONs the same, so when passing those as dict into the constructor, the corresponding fields are set. But it's possible that in Peaksel we add a new param, and this would break dict->DTO conversion as the param will be unknown. So to be forward-compatible, we add `**kwargs` to capture all the unknown fields.

# Work with source code

1. Install [uv](https://github.com/astral-sh/uv) build tool and run `uv build`
2. In PyCharm mark `src` as Source Root
3. To run the tests `./test.sh`