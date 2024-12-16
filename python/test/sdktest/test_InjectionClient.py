import unittest

from elsci.peakselsdk.dr.DetectorRun import AnalyticalMethod, DetectorType, IonMode, SpectrumCompression
from elsci.peakselsdk.plate.Plate import PlateLocation
from elsci.peakselsdk.signal.Range import FloatRange
from elsci.peakselsdk.substance.Substance import SubstanceChem
from sdktest.TestContext import peaksel
from sdktest.TestEnv import peaksel_username


class InjectionClientTest(unittest.TestCase):
    def test_upload_injection_with_spectra(self):
        resp = peaksel.injections().upload("resources/injections/agilent-chemstation-example.D.zip")
        self.assertEqual(1, len(resp))
        peaksel.substances().add(resp[0], SubstanceChem(mf="C6O6H12", alias="Test Alias"))

        j = peaksel.injections().get(resp[0])
        self.assertEqual(resp[0], j.eid)
        self.assertTestInjectionPropsExpected(j)
        self.assertSubstancePropsExpected(j)
        self.assertDrExpected(j)
        self.assertChromsExpected(j)
        self.assertDrDomainExpected(peaksel.blobs().get_detector_run_domain(j.detectorRuns[0].blobs.domain))
        self.assertSpectraExpected(peaksel.blobs().get_spectra(j.detectorRuns[0].blobs.spectra))
        print(j)

    def assertChromsExpected(self, j):
        self.assertEqual(2, len(j.chromatograms))
        self.assertEqual("MS SQD ScanMode EI+ Total", j.chromatograms[0].name)
        self.assertEqual(True, j.chromatograms[0].totalSignal)
        self.assertEqual([], j.chromatograms[0].massRange)
        self.assertNotEqual(0, len(j.chromatograms[0].baselineAnchors))
        self.assertEqual(j.detectorRuns[0].eid, j.chromatograms[0].detectorId)
        self.assertEqual("MS SQD ScanMode EI+ EIC", j.chromatograms[1].name)
        self.assertEqual(False, j.chromatograms[1].totalSignal)
        self.assertEqual(
            [FloatRange(179.56339, 180.56339), FloatRange(180.56674, 181.56674), FloatRange(181.56763, 182.56763)],
            j.chromatograms[1].massRange)
        self.assertNotEqual(0, len(j.chromatograms[1].baselineAnchors))
        self.assertEqual(j.detectorRuns[0].eid, j.chromatograms[1].detectorId)

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

    def assertSpectraExpected(self, spectra):
        self.assertEqual(3.0904500484466553, spectra[0].rt)
        self.assertEqual(10523.0, spectra[0].total_signal)
        self.assertEqual(32.099998474121094, spectra[0].base)
        self.assertEqual(25, len(spectra[0].x))
        self.assertEqual((30.100000381469727, 31.100000381469727), spectra[0].x[0:2])
        self.assertEqual(25, len(spectra[0].y))
        self.assertEqual((410.0, 1390.), spectra[0].y[0:2])

    def assertDrDomainExpected(self, x):
        self.assertEqual(8249, len(x))
        self.assertEqual(3.0904500484466553, x[0])

if __name__ == '__main__':
    unittest.main()
