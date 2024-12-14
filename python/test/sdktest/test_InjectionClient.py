import unittest

from elsci.peakselsdk.dr.DetectorRun import AnalyticalMethod, DetectorType, IonMode, SpectrumCompression
from elsci.peakselsdk.plate.Plate import PlateLocation
from elsci.peakselsdk.signal.Range import FloatRange
from elsci.peakselsdk.substance.Substance import SubstanceChem
from sdktest.TestContext import peaksel
from sdktest.TestEnv import peaksel_username


class InjectionClientTest(unittest.TestCase):
    def test_upload(self):
        resp = peaksel.injections().upload("resources/injections/agilent-chemstation-example.D.zip")
        self.assertEqual(1, len(resp))
        peaksel.substances().add(resp[0], SubstanceChem(mf="C6O6H12", alias="Test Alias"))

        j = peaksel.injections().get(resp[0])
        self.assertEqual(resp[0], j.eid)
        self.assertTestInjectionPropsExpected(j)
        self.assertSubstancePropsExpected(j)
        self.assertDrExpected(j)
        print(j)

    def assertDrExpected(self, j):
        self.assertEqual(1, len(j.detectorRuns))
        self.assertIsNotNone(j.detectorRuns[0].eid)
        self.assertEqual("m/z", j.detectorRuns[0].units)
        self.assertEqual(DetectorType.MS, j.detectorRuns[0].detectorType)
        self.assertEqual(AnalyticalMethod.MS, j.detectorRuns[0].analyticalMethod)
        self.assertEqual(0, j.detectorRuns[0].alignMin)
        self.assertEqual(30, j.detectorRuns[0].scanWindow.lower)
        self.assertEqual(300, j.detectorRuns[0].scanWindow.upper)
        self.assertEqual(IonMode.EIP, j.detectorRuns[0].ionMode)
        self.assertEqual("MS SQD ScanMode EI+", j.detectorRuns[0].description)
        self.assertIsNone(j.detectorRuns[0].seqNum)
        self.assertEqual(SpectrumCompression.CENTROIDED, j.detectorRuns[0].spectrumCompression)

    def assertSubstancePropsExpected(self, j):
        self.assertEqual(1, len(j.substances))
        self.assertIsNotNone(j.substances[0].eid)
        self.assertEqual("C6O6H12", j.substances[0].mf)
        self.assertEqual(180.06339, j.substances[0].emw)
        self.assertEqual("Test Alias", j.substances[0].alias)
        self.assertIsNone(j.substances[0].color)
        self.assertIsNone(j.substances[0].structureId)

    def assertTestInjectionPropsExpected(self, j):
        self.assertEqual("Dendro001", j.name)
        self.assertEqual("GC-MSD 68", j.instrumentName)
        self.assertEqual("GC ALKALOIDSMABELSPLIT", j.methodName)
        self.assertIsNotNone(j.creator.eid)
        self.assertEqual(peaksel_username(), j.creator.name)
        self.assertEqual(PlateLocation(0, 0), j.plateLocation)


if __name__ == '__main__':
    unittest.main()
