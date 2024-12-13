import unittest

from elsci.peakselsdk.InjectionClient import InjectionClient
from python.test.TestContext import peaksel


class InjectionClientTest(unittest.TestCase):
    def test_upload(self):
        injections = self._injection_client()
        resp = injections.upload("resources/injections/agilent-chemstation-example.D.zip")
        self.assertEqual(1, len(resp))

    def _injection_client(self) -> InjectionClient:
        return peaksel.injections()

if __name__ == '__main__':
    unittest.main()
