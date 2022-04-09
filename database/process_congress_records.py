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
        dataframe = pd.read_table(f"{year}FD.txt")

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

