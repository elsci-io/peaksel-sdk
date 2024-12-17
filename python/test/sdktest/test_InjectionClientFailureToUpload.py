import unittest

from sdktest.TestContext import peaksel


class InjectionClientTest(unittest.TestCase):
    def test_errs_if_error_happens_during_upload(self):
        try:
            peaksel.injections().upload("resources/injections/agilent-chemstation-example-fail.D.zip")
        except Exception as e:
            self.assertTrue(e.args[0].startswith("Not all injections were created successfully:"))
            return
        self.fail("The error didn't occur!")

if __name__ == '__main__':
    unittest.main()
