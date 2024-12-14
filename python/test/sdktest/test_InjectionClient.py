import unittest

from elsci.peakselsdk.plate.Plate import PlateLocation
from elsci.peakselsdk.substance.Substance import Substance
from sdktest.TestContext import peaksel
from sdktest.TestEnv import peaksel_username


class InjectionClientTest(unittest.TestCase):
    def test_upload(self):
        resp = peaksel.injections().upload("resources/injections/agilent-chemstation-example.D.zip")
        self.assertEqual(1, len(resp))
        peaksel.substances().add(resp[0], Substance(None, None, mf="C6O6H12"))

        j = peaksel.injections().get(resp[0])
        self.assertEqual(resp[0], j.eid)
        self.assertEqual("Dendro001", j.name)
        self.assertEqual("GC-MSD 68", j.instrumentName)
        self.assertEqual("GC ALKALOIDSMABELSPLIT", j.methodName)
        self.assertIsNotNone(j.creator.eid)
        self.assertEqual(peaksel_username(), j.creator.name)
        self.assertEqual(PlateLocation(0, 0), j.plateLocation)
        self.assertEqual(1, len(j.substances))
        self.assertIsNotNone(j.substances[0].eid)
        self.assertEqual("C6O6H12", j.substances[0].mf)
        self.assertEqual(180.06339, j.substances[0].emw)
        print(j)

if __name__ == '__main__':
    unittest.main()
