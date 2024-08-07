# Power BI XMLA Endpoint Download to Parquet

This package allows you to fetch and save Power BI tables in Parquet format via the XMLA endpoint.

## System Requirements

This package requires a Windows environment with .NET assemblies, as it relies on `pythonnet` to interact with .NET libraries.

## Authentication

The package currently only supports authentication using the Microsoft Authentication Library (MSAL) to obtain an access token, supporting Multi-Factor Authentication (MFA).


## Python Version Requirement

This package requires Python version >=3.9,<3.13.

## Installation

### Using Poetry

To install the package using Poetry, run:

poetry add download_pbi_xmla

### Using pip

To install the package using pip, run:

pip install download_pbi_xmla

## Setup

You can create the required .env and config.json files using the templates below, or you can run the scripts below to create the templates.

1. **Run the Setup Script**: This script will copy example configuration files and prompt you to edit them.

### Using Poetry

poetry run setup-files 

### Using pip

python -m download_pbi_xmla.setup_files


2. **Edit the .env and config.json files** with your credentials and configuration.

### .env File Example

CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
TENANT_ID=your-tenant-id
CONFIG_FILE=config.json
SAVE_PATH=./data

### config.json File Example

{
  "server": "your-server-url",
  "database": "your-database-name",
  "tables": [
    {
      "name": "your-table-name",
      "refresh_type": "full",
      "date_column": "your-date-column",
      "last_date": "YYYY-MM-DD"
    }
  ]
}

## Usage

After setting up the environment and configuration files, you can use the download.py script to fetch and save Power BI tables in Parquet format.

3. **Run the Download Script**: This script will load the environment variables and run the download process.

### Using poetry

poetry run run-download

### Using pip

python -m download_pbi_xmla.run_download


## Contribution

Feel free to fork the repository and create pull requests. Contributions are welcome!

For any issues or feature requests, please open an issue on the repository.