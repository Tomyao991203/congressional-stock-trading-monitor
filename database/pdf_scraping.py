import os
import PyPDF2
import tabula as tb
import copy
import json


def check_if_pdf_is_malformed(path: str):
    """
    takes in a path to a financial disclosure pdf. It then checks the size, as malformed pdfs are less than 2 kilobytes,
    and correctly formatted pdfs are much larger.

    :param path: str, path to pdf
    :return: boolean, whether pdf is malformed, which is when a pdf is "empty".
    """
    return os.stat(path).st_size <= 2000


def create_correct_template(file: str):
    """
    Because of the varied length and size of financial disclosure forms, we need to adjust the size of the template
    that scrapes the pdf for data. What this does is modifies the template for the individual financial disclosure form
    to make sure that we get all the correct information. It writes the temporary template to
    pdf_tmp_template.tabula-template.json. To learn more about what this template does, check out the tabula
    documentation for read_pdf_with_template().

    :param file: str, path to the financial disclosure pdf
    :returns: none, creates a temporary template called pdf_tmp_template.tabula-template.json
    """
    file = open(file, 'rb')
    readpdf = PyPDF2.PdfFileReader(file)
    total_pages = readpdf.numPages
    with open("database/pdf_reduced_template.tabula-template.json", "r") as jsonTemplate:
        data = json.load(jsonTemplate)
        page_template = data[3]
        if total_pages == 1:
            data = data[:-1]
        else:
            for page_num in range(2, total_pages):
                tmp_page_template = copy.copy(page_template)
                tmp_page_template['page'] = page_num + 1
                data.append(tmp_page_template)

        with open("database/pdf_tmp_template.tabula-template.json", 'w') as outfile:
            json.dump(data, outfile)


def pdf_discriminator(file: str):
    """
    takes in string to a financial disclosure pdf. Because there are multiple forms that are returned by the U.S.
    government as financial disclosures, we need to make sure that we are only using the correct form. If the pdf
    is the correct form type, it scrapes the data and returns a list of unprocessed pandas dataframes. If it is not,
    it prints the reason why the pdf file provided is incorrect, and returns none.

    :param file: str, path to financial disclosure form
    :return: if the pdf is the correct, returns the list of unprocessed pandas dataframes, if not returns None type.
    """
    if check_if_pdf_is_malformed(file):
        print(f"The path {file} leads to a malformed pdf.")
        return None

    create_correct_template(file)
    template_path = 'database/pdf_tmp_template.tabula-template.json'
    pdf_db = tb.read_pdf_with_template(file, template_path, stream=True)
    if pdf_db == [] or pdf_db[0].columns[0].lower() != 'filer information':
        print(f"The path {file} leads to a disclosure form of the incorrect format.")
        return None
    return pdf_db
