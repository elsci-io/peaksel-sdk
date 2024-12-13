import os


def envvar(varname: str, default_if_none: str) -> str:
    val = envvar_optional(varname)
    if val is None:
        return default_if_none
    return val

def envvar_optional(varname: str) -> str|None:
    if varname in os.environ:
        return os.environ[varname]
    return None