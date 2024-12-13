import base64
from random import randint

from elsci.peakselsdk.HttpClient import HttpClient
from elsci.peakselsdk.Peaksel import Peaksel
from elsci.peakselsdk.org.Org import OrgWithId
from elsci.peakselsdk.org.OrgClient import OrgClient
from sdktest.TestEnv import envvar, peaksel_username


# There's a singleton `peaksel` defined at the bottom of this file - use that one so that you don't create orgs
# every time you create TestContext


def _init_peaksel() -> Peaksel:
    passwrd: str = envvar("PEAKSEL_USER_PASSWORD", "sdktest") # these work only for locally deployed instances
    auth_header_val: str = "Basic " + base64.b64encode(str.encode(f"{peaksel_username()}:{passwrd}")).decode("ascii")
    base_url = envvar("PEAKSEL_BASE_URL", "http://localhost:8080")
    default_headers = {"Authorization": auth_header_val}

    org = _create_random_org(base_url, default_headers)
    return Peaksel(base_url, org_id=org.id, default_headers=default_headers)


def _create_random_org(base_url, default_headers):
    orgs = OrgClient(HttpClient(base_url=base_url, default_headers=default_headers), org_id="does not matter")
    org: OrgWithId = orgs.create(str(randint(0, 2000000000)))
    return org


peaksel = _init_peaksel()
