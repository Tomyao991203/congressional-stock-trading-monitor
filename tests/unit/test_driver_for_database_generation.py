import unittest
from database.driver_for_database_generation import *
from os.path import exists


class DriverForDatabaseGenerationProcessGetPdf(unittest.TestCase):
    """
    This tests the __scrap_and_process(pdf_paths_list) in driver_for_database_generation
    """

    def test_default_case(self):
        process_get_pdf("csv_for_test_default_case", year=2015, doc_id=10010857)
        self.assertTrue(exists("database/csvs/csv_for_test_default_case.csv"))

