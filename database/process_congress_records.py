import pandas as pd
import time
import requests

dataframe = pd.read_table("2019FD.txt")

doc_id = dataframe.get("DocID")
last_names = dataframe.get("Last")
first_names = dataframe.get("First")

print(dataframe.columns)
for i in range(len(doc_id)):
    url = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2019/{doc_id[i]}.pdf"
    # print(url)
    response = requests.get(url)
    with open(f"2019_house_pdfs/{last_names[i]}_{first_names[i]}_{doc_id[i]}.pdf", "wb") as f:
        f.write(response.content)

