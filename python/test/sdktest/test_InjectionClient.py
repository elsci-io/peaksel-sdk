import unittest

from elsci.peakselsdk.injection.InjectionClient import InjectionClient
from elsci.peakselsdk.plate.Plate import PlateLocation
from sdktest.TestContext import peaksel
from sdktest.TestEnv import peaksel_username


class InjectionClientTest(unittest.TestCase):
    def test_upload(self):
        injections = self._injection_client()
        resp = injections.upload("resources/injections/agilent-chemstation-example.D.zip")
        self.assertEqual(1, len(resp))

        j = injections.get(resp[0])
        self.assertEqual(resp[0], j.eid)
        self.assertEqual("Dendro001", j.name)
        self.assertEqual("GC-MSD 68", j.instrumentName)
        self.assertEqual("GC ALKALOIDSMABELSPLIT", j.methodName)
        self.assertIsNotNone(j.creator.eid)
        self.assertEqual(peaksel_username(), j.creator.name)
        self.assertEqual(PlateLocation(0, 0), j.plateLocation)
        self.assertEqual(0, len(j.substances))
        print(j)

    def _injection_client(self) -> InjectionClient:
        return peaksel.injections()

if __name__ == '__main__':
    unittest.main()
