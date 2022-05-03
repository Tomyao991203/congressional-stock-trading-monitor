import pandas as pd
import time
import requests
import os, os.path


def safe_open_w(path):
    """
    Opens path in write mode, creating any needed folders along the way

    :param path: The filename to open
    :return: The opened file object
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, "wb")


def get_year(year):
    """
    takes in a year (2013-2022) and downloads all the financial disclosure pdfs into year_house_pdfs/ in the current
    directory

    :param year: int or string, between 2013-2022.
    :return: void, writes pdfs to year_house_pdf/
    """
    dataframe = pd.read_table(f"Financial_Disclosure_txt_files/{year}FD.txt")

    doc_id = dataframe.get("DocID")
    last_names = dataframe.get("Last")
    first_names = dataframe.get("First")

    print(dataframe.columns)
    for i in range(len(doc_id)):
        url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id[i]}.pdf"
        # print(url)
        response = requests.get(url)
        with safe_open_w(f"database/pdfs/{year}_house_pdfs/{last_names[i]}_{first_names[i]}_{doc_id[i]}.pdf") as f:
            f.write(response.content)


def get_pdf(year, last="", first="", doc_id=0):
    """
    get_pdf(year, last="", first="", doc_id=0) takes in one mandatory argument (year), and three optional arguments,
    (last, first, doc_id). However, either last and first or doc_id must be provided.

    In the case of doc_id being provided, get_pdf() will download the corresponding financial disclosure form that
    corresponds to that document id. This will be saved in year_house_pdfs/ in the current directory.

    in the case of a first and last name being provided, get_pdf() will download all the financial disclosure forms
    that correspond to that member in the given year. All of the pdfs will be saved in the year_house_pdfs/.

    :param year: int or string of the year desired (2013-2022)
    :param last: last name of the house member, should be a string.
    :param first: first name of the house member, should be a string.
    :param doc_id: int or string of the document id.
    :return: void, writes the pdfs into year_house_pdfs/
    """
    if doc_id != 0:
        __get_pdf_doc_id(year, doc_id)

    else:
        if last == "" or first == "":
            print("Please provide either a last and first name, or a document id.")
            exit()

        __get_pdf_last_first_names(year, last=last, first=first)


def __get_pdf_doc_id(year, doc_id):
    """
    private helper function for get_pdf(), when a doc_id is provided. Like stated above, __get_pdf_doc_id() will
    download the corresponding financial disclosure form that
    corresponds to that document id. This will be saved in year_house_pdfs/ in the current directory.

    :param year: int or string of the year desired (2013-2022)
    :param doc_id: int or string of the document id.
    :return: void, writes the pdfs into year_house_pdfs/
    """
    dataframe = pd.read_table(f"database/Financial_Disclosure_txt_files/{year}FD.txt")

    record = dataframe.loc[dataframe['DocID'] == doc_id]
    last_name = record['Last'].values[0]
    first_name = record['First'].values[0]

    url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id}.pdf"
    # print(url)
    response = requests.get(url)
    with safe_open_w(f"database/pdfs/{year}_house_pdfs/{last_name}_{first_name}_{doc_id}.pdf") as f:
        f.write(response.content)


def __get_pdf_last_first_names(year, last, first):
    """
    private helper function for get_pdf(). __get_pdf_last_first_names() will download all the financial disclosure forms
    that correspond to that member of the house  in the given year. All of the pdfs will be saved in
    the year_house_pdfs/.

    :param year: int or string of the year desired (2013-2022)
    :param last: last name of the house member, should be a string.
    :param first: first name of the house member, hsould be a string.
    :return: void, writes the pdfs into year_house_pdfs/

    """
    dataframe = pd.read_table(f"database/Financial_Disclosure_txt_files/{year}FD.txt")
    dataframe['Last'] = dataframe['Last'].apply(str.lower)
    dataframe['First'] = dataframe['First'].apply(str.lower)
    last_df = dataframe.loc[dataframe['Last'] == str.lower(last)]
    last_first_df = last_df.loc[last_df['First'] == str.lower(first)]

    doc_id = last_first_df.get("DocID").values

    for i in range(len(doc_id)):
        url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id[i]}.pdf"
        # print(url)
        response = requests.get(url)
        with safe_open_w(f"database/pdfs/{year}_house_pdfs/{last}_{first}_{doc_id[i]}.pdf") as f:
            f.write(response.content)
