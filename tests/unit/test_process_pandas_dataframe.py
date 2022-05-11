import unittest
from database.process_pandas_dataframe import *
from database.pdf_scraping import *


class ProcessPandasDataframeFindStart(unittest.TestCase):
    """
    tests the find_start function of process_pandas_dataframe
    """

    def test_find_start_default_working_case(self):
        """
        tests when "schedule b: transaction" is actually in the dataframe
        """
        df = pdf_discriminator("database/2015_house_pdfs/Pelosi_Nancy_10010857.pdf")
        find_start_result = find_start(df)
        self.assertTrue(find_start_result is not None)
