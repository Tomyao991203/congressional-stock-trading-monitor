# Congressional Stock Trading Monitor

The Congressional Stock Trading Monitor will be a tool that assists users in collecting, parsing and viewing data about stock market transactions that members of the U.S. House of Representatives publically report.

## How To Run the Software

### A. Running Software Through a Docker Container

1. Open docker and a terminal window to this folder
2. Type the following docker commands into the terminal window:
    * ```docker compose build```
    * ```docker-compose up```
3. Visit http://127.0.0.1:5000/  or localhost:5000 in a browser to see the webpage.

### B. Visiting the Website

If the Congressional Stock Trading Monitor is running on our server, you can access the webpage through http://35.175.242.206:5000.

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

### *db* Directory
The ```db``` directory contains database files.

### *templates* Directory
The ```templates``` directory contains html files.
* ```index.html```: html file defining the front-end structure of the home page.

### *static* Directory
The ```static``` directory contains any scripts, css, and javascript files.
* ```style.css```: css file defining the style of the webpage

### *tests* Directory
The ```tests``` directory contains all test files.
* ```unit``` directory: contains all unit tests
    * ```text_proxy.py```: tests the ```Proxy``` class *[currently a placeholder for more tests to come in the future as the application is developed]*

### Docker Files
1. ```Dockerfile```: text file that includes instructions to automatically install and configure the Docker image.
2. ```compose.yaml```: configuration file that defines services, networks, and volumes for Docker containers.
3. ```requirements.txt```: text file storing all the information about libraries, modules, and packages that are required for this webpage. This file is used by Docker to build the Docker image.

## Level of Effort by Each Member
