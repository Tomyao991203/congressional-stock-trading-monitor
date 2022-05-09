from pdf_scraping import *
from process_pandas_dataframe import *
from process_congress_records import *


def __scrap_and_process(pdf_paths_list):
    """

    Takes in a list of pdf paths (stored locally) to a financial disclosure pdf. It checks if they pdfs are valid,
    then scrapes the data and processes it. It will return the data as a pandas dataframe.

    :pdf_paths_list): list of str, paths to financial disclosure forms
    :return: a pandas dataframe with the processed dada from the given pdfs.
    """
    index = 0
    unprocessed_db = pdf_discriminator(pdf_paths_list[index])
    while unprocessed_db is None and index < len(pdf_paths_list)-1:
        index += 1
        unprocessed_db = pdf_discriminator(pdf_paths_list[index])

    if unprocessed_db is None:
        print("The list of pdf paths were all invalid pdf forms")
        return None

    final_db = process_dataframe(unprocessed_db, pdf_paths_list[0])
    for pdf_path in pdf_paths_list[1:]:
        unprocessed_db = pdf_discriminator(pdf_path)
        if unprocessed_db is not None:
            processed_db = process_dataframe(unprocessed_db, pdf_path)
            final_db = pd.concat([final_db, processed_db])

    return final_db


def process_get_pdf(year, last="", first="", doc_id=0):
    get_pdf(year, last, first, doc_id)

