
Database
--------
The `database` directory contains database files, python files for webscraping, and resulting pdf and text files \
from webscraping.

* `pdfs` directory: contains pdf files of stock transactions records for the U.S. House of Representatives.
* `Financial_Disclosure_txt_files` directory: contains text files of the U.S. House of Representatives, separated by year.
* `process_congress_records.py`: python file that scrapes the U.S. House of Representatives member names and stores them
  as text files in the Financial_Disclosure_txt_files directory; the python file also scrapes pdf files of stock
  transaction records for U.S. House of Representatives members and stores them in the pdf directory.
* `sample_data.csv`: contains real stock transactions for 32 U.S. House of Representatives.
* `database.db`: database file.
* `database_schema.sql`: sql file that adds a table to the database to store all transactions.
* `create_database_version1.ipynb`: python notebook that updates the database with data.
* `pdf_scraping.py`: python file that will eventually contain all the functions for pdf scraping.
* `pdf_scraper_notebook.ipynb`: a python jupyter notebook that contains all the work for the creating the pdf scraping
  functions.
* `json` files all the json files are used for tabula templates, which help with parsing the pdfs.

PDF Scraping
^^^^^^^^^^^^
`pdf_scraping.py`: python file that contains all the functions for pdf scraping.

.. automodule:: database.pdf_scraping
    :members:

Process Congress Records
^^^^^^^^^^^^^^^^^^^^^^^^
`process_congress_records.py`: python file that scrapes the U.S. House of Representatives member names and stores \
them as text files in the Financial_Disclosure_txt_files directory; the python file also scrapes pdf files of stock \
transaction records for U.S. House of Representatives members and stores them in the pdf directory.

.. automodule:: database.process_congress_records
    :members: