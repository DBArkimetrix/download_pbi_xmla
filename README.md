# Power BI XMLA Endpoint Download to Parquet

This package allows you to fetch and save Power BI tables in Parquet format via the XMLA endpoint.

## System Requirements

This package requires a Windows environment with .NET assemblies, as it relies on `pythonnet` to interact with .NET libraries.
Latest version 

## Python Version Requirement

This package requires Python version >=3.9,<3.13.

## Installation

### Using Poetry

To install the package using Poetry, run:

poetry add download_pbi_xmla

### Using pip

To install the package using pip, run:

pip install download_pbi_xmla

## Usage
After installing the package, you can use the fetch_tables command to download and save Power BI tables in Parquet format.
Below are the details on how to use the command.

### Command Syntax

fetch_tables --server SERVER_URL --db_name DATABASE_NAME --username USERNAME --password PASSWORD --tables Table1 Table2 --path PATH_TO_SAVE [--use_mfa]

### Parameters
--server: The XMLA endpoint URL for your Power BI service.
--db_name: The name of the database you want to connect to.
--username: Your username for the Power BI service.
--password: Your password for the Power BI service.
--tables: The list of tables you want to fetch. You can specify multiple tables separated by spaces.
--path: The path where the Parquet files will be saved.
--use_mfa: (Optional) Use Multi-Factor Authentication for authentication. If not specified, it will use just the username and password for authentication.

### Example 

#### Without MFA

fetch_tables --server "powerbi://api.powerbi.com/v1.0/myorg/YourWorkspace" --db_name "YourDatabaseName" --username "YourUsername" --password "YourPassword" --tables "Table1" "Table2" --path "C:/Users/dbhar/Documents/download_test"

#### With MFA
fetch_tables --server "powerbi://api.powerbi.com/v1.0/myorg/YourWorkspace" --db_name "YourDatabaseName" --username "YourUsername" --password "YourPassword" --tables "Table1" "Table2" --path "C:/Users/dbhar/Documents/download_test" --use_mfa

## Authentication

The package supports two modes of authentication:

Without MFA: Uses just the username and password provided.
With MFA: Uses the Microsoft Authentication Library (MSAL) to obtain an access token, supporting Multi-Factor Authentication (MFA).




