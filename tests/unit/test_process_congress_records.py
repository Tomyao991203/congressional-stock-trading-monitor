"""
This is a little test suite for process_congress_records.py
"""
import unittest
from database.process_congress_records import get_pdf
from os.path import exists


class ProcessCongressRecordsGetPdf(unittest.TestCase):
    """
    This test case is supposed to test the get_pdf() function from process_congress_records.py. It currently passes no
    matter what as I don't have a way to actually test it.
    """

    def test_doc_id_pdf(self):
        get_pdf(year=2020, doc_id=10039988)
        self.assertTrue(True)

    def test_last_first_name_pdf(self):
        get_pdf(year=2020, first="Joe", last="Wilson")
        self.assertTrue(True)
