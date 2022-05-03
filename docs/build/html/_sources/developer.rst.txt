Developer Documentation
=======================
The goal of this application is to utilize webscraping tools to gather information from the Financial Disclosures of \
U.S. House of Representatives into a database.
This database will be queried to provide structured and formatted data \
to users on the webpage, along with unique visualizations.
The website containing information pertaining to the Financial Disclosures of U.S. House of Representatives can be \
found at: https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure.
Our current application holds a pre-populated database of real stock transactions from \
the U.S. House of Representatives.
The database holds the following information for \
32 U.S. House of Representatives: Representative Name, State District Number, Company, Ticker, \
Transaction Type, Date, Amount, and Description.
This application utilizes a Continuous Integration and Continuous Delivery pipeline to automate tests.

.. toctree::
   :maxdepth: 3

   cstm
   database
   templates
   static
   tests