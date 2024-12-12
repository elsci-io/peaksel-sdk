import unittest

from elsci.peakselsdk.InjectionClient import InjectionClient
from elsci.peakselsdk.Peaksel import Peaksel


class InjectionClientTest(unittest.TestCase):
    def test_something(self):
        injections = self._injection_client()
        resp = injections.upload("/Users/stas/peaksel/waters/1234567-0001.raw.zip")
        self.assertEqual(1, len(resp))

    def _injection_client(self) -> InjectionClient:
        return Peaksel("http://localhost:8080", "8e8U3eYyNuL",
                       {}).injections()

if __name__ == '__main__':
    unittest.main()
