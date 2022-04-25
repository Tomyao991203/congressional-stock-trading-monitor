import unittest

from cstm.dataclasses import District
from cstm.enums import State


class DistrictFromStringTestCase(unittest.TestCase):

    def test_from_district_string_exception_on_invalid_input(self):
        invalid_strings = ["CZ00", "MD100", "C0", "ca01", "district"]
        for s in invalid_strings:
            with self.assertRaises(Exception):
                District.from_district_string(s)

    def test_from_district_string_with_sample_inputs(self):
        strings = ["CA01", "MD02", "TX03", "NM04", "NM05"]
        districts = [District(State.CALIFORNIA, 1), District(State.MARYLAND, 2),
                     District(State.TEXAS, 3), District(State.NEW_MEXICO, 4),
                     District(State.NEW_MEXICO, 5)]

        for i in range(len(strings)):
            self.assertEqual(districts[i], District.from_district_string(strings[i]))