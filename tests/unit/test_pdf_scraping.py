import unittest
from database.pdf_scraping import *
from os.path import exists


class PdfScrapingCheckIfPdfIsMalformed(unittest.TestCase):
    """
    This test case checks the check_if_pdf_is_malformed() from pdf_scraping.py
    """

    def test_malformed_input(self):
        db_malformed = check_if_pdf_is_malformed("database/2015_house_pdfs/Pelosi_Nancy_20002351.pdf")
        self.assertTrue(db_malformed)

    def test_not_malformed_input(self):
        db = check_if_pdf_is_malformed("database/2015_house_pdfs/Pelosi_Nancy_10010857.pdf")
        self.assertFalse(db)


class PdfScrapingCreateCorrectTemplate(unittest.TestCase):
    """
    This test case checks the create_correct_template() from pdf_scraping.py
    """

    def test_correct_template(self):
        create_correct_template("database/2015_house_pdfs/Pelosi_Nancy_10010857.pdf")
        self.assertTrue(exists("database/pdf_tmp_template.tabula-template.json"))


class PdfScrapingPdfDiscriminator(unittest.TestCase):
    """
    Tests pdf_discriminator() from pdf_scraping.py
    """

    def test_malformed_input(self):
        db = pdf_discriminator("database/2015_house_pdfs/Pelosi_Nancy_20002351.pdf")
        self.assertTrue(db is None)

    def test_working_input(self):
        db = pdf_discriminator("database/2015_house_pdfs/Pelosi_Nancy_10010857.pdf")
        first_line_check = db[0].columns[0].lower() == 'filer_information'
        self.assertTrue(first_line_check)

    def test_not_malformed_but_incorrect_form(self):
        db = pdf_discriminator("database/2015_house_pdfs/Adams_Boyce_9106272.pdf")
        self.assertTrue(db is None)
