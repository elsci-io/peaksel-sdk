import unittest

from sdktest.TestContext import peaksel


class InjectionClientTest(unittest.TestCase):

    def test_listing_orphan_injections(self):
        resp = peaksel.injections().upload("resources/injections/agilent-chemstation-example.D.zip")
        self.assertEqual(1, len(resp))
        inj_id: str = resp[0]
        name = peaksel.injections().get(inj_id).name
        # Check finds uploaded injection in the latest
        self.assertEqual(inj_id, peaksel.injections().list_orphan()[0].eid)
        # Check searching by name finds:
        self.assertEqual(inj_id, peaksel.injections().list_orphan(name_starting_with=name, page=0)[0].eid)
        # Check pagination skips the first page:
        self.assertEqual(0, len(peaksel.injections().list_orphan(name_starting_with=name, page=100)))
        # Check name filters out:
        self.assertEqual(0, len(peaksel.injections().list_orphan(name_starting_with="blah blah pam param")))


if __name__ == '__main__':
    unittest.main()
