from random import randint

from peakselsdk.HttpClient import HttpClient
from peakselsdk.Peaksel import Peaksel
from peakselsdk.org.Org import OrgShort
from peakselsdk.org.OrgClient import OrgClient
from peakselsdk.util.api_util import peaksel_basic_auth_header
from sdktest.TestEnv import envvar, peaksel_username


# There's a singleton `peaksel` defined at the bottom of this file - use that one so that you don't create orgs
# every time you create TestContext


def _init_peaksel() -> Peaksel:
    passwrd: str = envvar("PEAKSEL_USER_PASSWORD", "sdktest") # these work only for locally deployed instances
    auth_header_val: str = peaksel_basic_auth_header(peaksel_username(), passwrd)
    base_url = envvar("PEAKSEL_BASE_URL", "http://localhost:8080")
    default_headers = {"Authorization": auth_header_val}

    org = _create_random_org(base_url, default_headers)
    return Peaksel(base_url, org_id=org.id, default_headers=default_headers)


def _create_random_org(base_url, default_headers):
    orgs = OrgClient(HttpClient(base_url=base_url, default_headers=default_headers))
    org: OrgShort = orgs.create(str(randint(0, 2000000000)))
    return org


peaksel = _init_peaksel()
