"""
This is a little test suite for process_congress_records.py
"""
import unittest
from database.process_congress_records import get_pdf
from os.path import exists


class ProcessCongressRecordsGetPdf(unittest.TestCase):
    """
    This test case is supposed to test the get_pdf() function from process_congress_records.py.
    """

    def test_doc_id_pdf(self):
        get_pdf(year=2020, doc_id=10039988)
        self.assertTrue(exists("database/pdfs/2020_house_pdfs/Pelosi_Nancy_10039988.pdf"))

    def test_last_first_name_pdf(self):
        get_pdf(year=2020, first="Joe", last="Wilson")
        self.assertTrue(exists("database/pdfs/2020_house_pdfs/Wilson_Joe_30014807.pdf"))
        self.assertTrue(exists("database/pdfs/2020_house_pdfs/Wilson_Joe_10040196.pdf"))
