# Power_Plant_Api

Provide data on power plant per request at the backend.

## Set up virtual environment

Install virtualenv package as follows:

`pip install virtualenv`

Set up and activate virtual environment `venv` in a terminal:

`virtualenv venv`

`source venv/bin/activate`

## Install required packages

`pip install -r requirements.txt`

## Get raw data

The data comes as excel file after unzip -  https://www.epa.gov/energy/emissions-generation-resource-integrated-database-egrid (eGRID2018 Data File)

## Parse data from excel into sqlite database

Run the following command in a terminal:

`xls2db egrid2018_data.xlsx egrid2018_data.db`

In sqlite command-line interface, remove the first row caused by the filter in excel using DELETE statement.

## Run backend application

In a terminal of this application folder, run the following:

`python application.py`

Then in a web browser, request the data as describe in the API.
