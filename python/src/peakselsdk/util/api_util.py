import base64


def peaksel_basic_auth_header(username: str, password: str):
    """
    Basic Auth credentials can be set up in the config file: https://elsci.io/docs/peaksel/security/users.html#inmemory-users
    If you want to work with Hub/SaaS, then let us know (support@elsci.io), and we can set up creds for you.
    :param username: the user configured in Peaksel during the startup
    :param password: the password of that user in plain text
    :return: HTTP header value to be passed to Authorization header
    """
    return "Basic " + base64.b64encode(str.encode(f"{username}:{password}")).decode("ascii")