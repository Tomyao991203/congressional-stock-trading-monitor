import pandas as pd
import re

import tabula as tb


def scrape_pdf(file):
    template_path = 'pdf_template.tabula-template.json'
    df = tb.read_pdf_with_template(file, template_path, stream=True)
    print(df[7])


pdf_path = "2015_house_pdfs/Pelosi_Nancy_10010857.pdf"
scrape_pdf(pdf_path)
