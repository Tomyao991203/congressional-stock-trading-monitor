# Congressional Stock Trading Monitor

The Congressional Stock Trading Monitor will be a tool that assists users in collecting, parsing and viewing data about stock market transactions that members of the U.S. House of Representatives publically report.

## How To Run the Software

### A. Running Software Through a Docker Container

1. Open docker and a terminal window to this folder
2. Type the following docker commands into the terminal window:
    * ```docker-compose build && docker-compose up```
3. Visit http://127.0.0.1:5000/  or localhost:5000 in a browser to see the webpage.
4. When finished, run `docker-compose down` to remove leftover container artifacts.

### B. Visiting the Website

You can visit the Congressional Stock Trading Monitor webpage [here](http://cstm-testing.eba-2jr5ivme.us-east-1.elasticbeanstalk.com/).

## User Documentation

On the front page of the Congressional Stock Trading Monitor webpage, users can input different searches to get information and data pertaining to the U.S. House of Representatives stock market transactions. The user interface allows users to search by *Representative Name*, *State District Number*, *Company*, *Transaction Type*, and *Year*.

In future updates, the User Interface will also contain a *Menu Button* that allows users to navigate to different pages of the Congressional Stock Trading Monitor. These pages include:
1. List of Transactions
2. List of U.S. House of Representatives
3. List of Companies

***Searches that are currently supported:***
1. Select a year to see a list of all the House members that traded within that year.

## Developer Documentation
The goal of this application is to utilize webscraping tools to gather information from the Financial Disclosures of U.S. House of Representatives into a database. This database will be queried to provide structured and formatted data to users on the webpage, along with unique visualizations. *The website containing information pertaining to the Financial Disclosures of U.S. House of Representatives can be found at: https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure.*

Our current application holds a pre-populated database of real stock transactions from the U.S. House of Representatives. The database holds the following information for 32 U.S. House of Representatives: *Representative Name*, *State District Number*, *Company*, *Ticker*, *Transaction Type*, *Date*, *Amount*, and *Description*.

This application utilizes a *Continuous Integration* and *Continuous Delivery* pipeline to automate tests.  

The repository ```congressional-stock-trading-monitor``` consists of:

### *app.py* File
The ```app.py``` file uses the Flask framework to create the web application.

### *ctsm* Directory
The ```ctsm``` directory contains backend python files to retreive, modify, and send information to the Flask application.
1. ```view_interface.py```: includes an abstract base class ```ViewInterface``` that defines the interface for the views of the webpage. 
2. ```input_validator.py```: includess an abstract base class ```InputValidator``` that validates inputs of the webpage.
3. ```proxy.py```: includes a class ```Proxy``` that acts as a mediator between the Flask application and python backend.
4. ```query.py```: contains a function that returns a key-value pair as a string to assist with database queries.
5. ```database_helpers.py```: connects html code form requests with queries on the database.
6. ```representative_helpers.py```: contains code responsible for obtaining and processing representative information
7. ```enums.py```: Contains enumerated types found in CSTM
8. ```dataclasses.py```: Contains dataclasses found in CSTM

### *database* Directory
The ```database``` directory contains database files, python files for webscraping, and resulting pdf and text files from webscraping.
1. ```pdfs``` directory: contains pdf files of stock transactions records for the U.S. House of Representatives.
2. ```Financial_Disclosure_txt_files``` directory: contains text files of the U.S. House of Representatives, separated by year.
3. ```process_congress_records.py```: python file that scrapes the U.S. House of Representatives member names and stores them as text files in the ```Financial_Disclosure_txt_files``` directory; the python file also scrapes pdf files of stock transaction records for U.S. House of Representatives members and stores them in the ```pdf``` directory. 
4. ```sample_data.csv```: contains real stock transactions for 32 U.S. House of Representatives.
5. ```database.db```: database file.
6. ```database_schema.sql```: sql file that adds a table to the database to store all transactions.
7. ```create_database_version1.ipynb```: python notebook that updates the database with data.

### *templates* Directory
The ```templates``` directory contains html files.
* ```partials``` directory: contains html files defining reusable UI components
    * ```description_modal.html```: html file defining the transaction description popup
    * ```navigation_bar.html```: html file defining the responsive navigation
    * ```transaction_table.html```: html file defining the transaction table
* ```base.html```: html file defining the basic webpage format to extend into other pages
* ```transactions.html```: html file defining the transaction driven view

### *static* Directory
The ```static``` directory contains any scripts, css, and javascript files.
* ```darkly.bootstrap.min.css```: css file with the darkly bootstrap theme
* ```flatly.bootstrap.min.css```: css file with the darkly bootstrap theme

### *tests* Directory
The ```tests``` directory contains all test files.
* ```unit``` directory: contains all unit tests
    1. ```test_process_congress_records.py```: tests that ```process_congress_records.py``` webscrapes pdf files.
    2. ```test_database_helpers.py```: tests the database created in ```database_helpers.py```.
    3. ```test_query.py```:  tests ```query.py```.
    4. ```text_proxy.py```: tests the ```Proxy``` class *[currently a placeholder for more tests to come in the future as the application is developed]*.
    5. ```test_state_enum.p```: tests the `State` enumerated type
    6. ```test_transaction_dataclass.py```: tests the Transaction dataclass
    7. ```test_disctrict_dataclasss.py```: tests the District dataclass
    8. ```test_state_enum.py```: tests the State enum
    9. ```test_representative_helpers.py```: tests the representative helper functions

### Docker Files
1. ```Dockerfile```: text file that includes instructions to automatically install and configure the Docker image.
2. ```compose.yaml```: configuration file that defines services, networks, and volumes for Docker containers.
3. ```requirements.txt```: text file storing all the information about libraries, modules, and packages that are required for this webpage. This file is used by Docker to build the Docker image.

## Level of Effort by Each Member
* (30%) Brian Spates - Organized group meetings, dealt with merge requests and resolving probelms before merging, setup AWS, setup CI/CD pipeline, wrote tests for the database code.
* (25%) Jiaming Yao - Responsible for all code regarding the database and connecting HTML forms to the querying the database. 
* (15%) Jake Wilson - Responsible for coding webscraping python files and corresponding tests.
* (15%) Xue Qiu - Responsible for writing documentation and some html/css code.
* (15%) Michelle Zheng - Responsible for some html code and collecting data entries into a .cvs file.
