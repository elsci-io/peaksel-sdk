import unittest

from peakselsdk.chromatogram.Chrom import Chrom
from peakselsdk.dr.DetectorRun import AnalyticalMethod, DetectorType, IonMode, SpectrumCompression
from peakselsdk.injection.Injection import InjectionShort, InjectionFull
from peakselsdk.plate.Plate import PlateLocation
from peakselsdk.signal.Range import FloatRange
from peakselsdk.substance.Substance import SubstanceChem, Substance
from sdktest.TestContext import peaksel
from sdktest.TestEnv import peaksel_username


class InjectionClientTest(unittest.TestCase):
    def test_upload_injection_with_spectra(self):
        resp = peaksel.injections().upload("resources/injections/agilent-chemstation-example.D.zip")
        self.assertEqual(1, len(resp))
        # Add analyte:
        inj_id: str = resp[0]
        peaksel.substances().add(inj_id, SubstanceChem(mf="C6O6H12", alias="Test Alias"))
        j: InjectionFull = peaksel.injections().get(inj_id)

        self.assertEqual(inj_id, j.eid)
        self.assertTestInjectionPropsExpected(j)
        self.assertSubstancePropsExpected(j)
        self.assertDrExpected(j)
        self.assertChromsExpected(j)
        self.assertDrDomainExpected(peaksel.blobs().get_detector_run_domain(j.detectorRuns[0].blobs.domain))
        self.assertSpectraExpected(peaksel.blobs().get_spectra(j.detectorRuns[0].blobs.spectra))

        c = j.chromatograms.filter_by_name("MS SQD ScanMode EI+ Total").get_single()
        self.assertChromSignalExpected(peaksel.blobs().get_chrom_signal(c.signalId))

        j = self.assertCanAddPeak(j)

        batch_id: str = peaksel.batches().assign_injections([j.eid], batch_name="some batch")
        j = peaksel.injections().get(j.eid)
        self.assertEqual(batch_id, j.batchId)

        batch_injs: list[InjectionShort] = peaksel.batches().get_injections(batch_id)
        self.assertEqual(1, len(batch_injs))
        self.assertTestInjectionPropsExpected(batch_injs[0])
        self.assertCanSetProps(j)
        self.assertCanCreateCustomChroms(j)
        print(j)

    def assertCanCreateCustomChroms(self, j):
        peaksel.chroms().add_chromatogram(j.eid, "Custom chrom",
                                          [0.1, .2, .3, .4, 1, 2, 3, 4], [1, 5, 7, 9, 2, 1, 1, 2])
        self.assertEqual(1, len(peaksel.injections().get(j.eid).chromatograms.filter_by_name("Custom chrom")))

    def assertCanSetProps(self, j: InjectionFull):
        self.assertEqual(0, len(j.userDefinedProps))
        props: dict[str, any] = {"str": "val", "num": 1, "null": None, "nested": {"key": "true"}}
        peaksel.injections().set_props(j.eid, props)
        self.assertDictEqual(props, peaksel.injections().get(j.eid).userDefinedProps)

    def assertCanAddPeak(self, j):
        substance: Substance = j.substances[0]
        chrom: Chrom = j.chromatograms[0]
        peaksel.peaks().add(j.eid, chrom.eid, substance.eid, 3500, 3700)
        j = peaksel.injections().get(j.eid)

        self.assertEqual(1, len(j.peaks))
        self.assertIsNotNone(1, j.peaks[0].eid)
        self.assertIsNotNone(substance.eid, j.peaks[0].substanceId)
        self.assertIsNotNone(chrom.eid, j.peaks[0].chromatogramId)
        self.assertIsNotNone(1, j.peaks[0].blobs.spectrum)
        self.assertTrue(j.peaks[0].area > 1000)
        self.assertTrue(j.peaks[0].areaPercent > .01)
        self.assertTrue(14 < j.peaks[0].rt < 16)
        self.assertEqual([3500, 3700], j.peaks[0].indexRange)
        self.assertTrue(3500 <= j.peaks[0].rtIdx <= 3700)

        peak_spectrum = peaksel.blobs().get_peak_spectrum(j.peaks[0].blobs.spectrum)
        self.assertEqual(667, len(peak_spectrum))
        self.assertEqual(30.100000381469727, peak_spectrum.x[0])
        self.assertEqual(5.616915702819824, peak_spectrum.y[0])
        return j

    def assertChromsExpected(self, j):
        tic = (j.chromatograms.filter_by_detector_run(j.detectorRuns.filter_by_type(DetectorType.MS)[0].eid)
             .filter_total()
             .get_single())
        self.assertEqual(tic, j.chromatograms.filter_by_name("MS SQD ScanMode EI+ Total").get_single())

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

    def assertChromSignalExpected(self, signal: tuple[float,...]):
        self.assertEqual(8249, len(signal))
        self.assertEqual(10523.0, signal[0])


if __name__ == '__main__':
    unittest.main()
