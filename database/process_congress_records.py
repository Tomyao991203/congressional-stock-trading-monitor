import pandas as pd
import time
import requests


def get_year(year):
    dataframe = pd.read_table(f"Financial_Disclosure_txt_files/{year}FD.txt")

    doc_id = dataframe.get("DocID")
    last_names = dataframe.get("Last")
    first_names = dataframe.get("First")

    print(dataframe.columns)
    for i in range(len(doc_id)):
        url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id[i]}.pdf"
        # print(url)
        response = requests.get(url)
        with open(f"{year}_house_pdfs/{last_names[i]}_{first_names[i]}_{doc_id[i]}.pdf", "wb") as f:
            f.write(response.content)


def get_pdf(year, last="", first="", doc_id=0):
    if doc_id != 0:
        __get_pdf_doc_id(year, doc_id)

    else:
        if last == "" or first == "":
            print("Please provide either a last and first name, or a document id.")
            exit()

        __get_pdf_last_first_names(year, last=last, first=first)


def __get_pdf_doc_id(year, doc_id):
    dataframe = pd.read_table(f"Financial_Disclosure_txt_files/{year}FD.txt")

    record = dataframe.loc[dataframe['DocID'] == doc_id]
    last_name = record['Last'].values[0]
    first_name = record['First'].values[0]

    url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id}.pdf"
    # print(url)
    response = requests.get(url)
    with open(f"{year}_house_pdfs/{last_name}_{first_name}_{doc_id}.pdf", "wb") as f:
        f.write(response.content)


def __get_pdf_last_first_names(year, last, first):
    dataframe = pd.read_table(f"Financial_Disclosure_txt_files/{year}FD.txt")
    dataframe['Last'] = dataframe['Last'].apply(str.lower)
    dataframe['First'] = dataframe['First'].apply(str.lower)
    last_df = dataframe.loc[dataframe['Last'] == str.lower(last)]
    last_first_df = last_df.loc[last_df['First'] == str.lower(first)]

    doc_id = last_first_df.get("DocID").values

    for i in range(len(doc_id)):
        url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}/{doc_id[i]}.pdf"
        # print(url)
        response = requests.get(url)
        with open(f"{year}_house_pdfs/{last}_{first}_{doc_id[i]}.pdf", "wb") as f:
            f.write(response.content)
