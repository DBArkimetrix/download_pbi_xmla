from main import fetch_tables
import argparse
import sys
from dotenv import load_dotenv
import os
import logging
import time
from datetime import datetime
import pandas as pd
import numpy as np

# Create a logs directory if it does not exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to file with a datestamp
log_filename = datetime.now().strftime("logs/log_%Y%m%d_%H%M%S.log")
logging.basicConfig(filename=log_filename, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Also set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Load environment variables from .env file
load_dotenv()

# Fetch secrets and other settings from environment variables
CLIENT_ID = os.getenv('CLIENT_ID').strip()
CLIENT_SECRET = os.getenv('CLIENT_SECRET').strip()
TENANT_ID = os.getenv('TENANT_ID').strip()
SERVER = os.getenv('SERVER').strip()
DB_NAME = os.getenv('DB_NAME').strip()
TABLES = os.getenv('TABLES').strip()
if TABLES:
    TABLES = TABLES.split(',')
SAVE_PATH = os.getenv('SAVE_PATH')

if SAVE_PATH:
    SAVE_PATH = SAVE_PATH.strip()
else:
    SAVE_PATH = ''  # Provide a default value or handle the absence appropriately

# Debug print statements to verify environment variables
logging.debug(f"CLIENT_ID: {CLIENT_ID}")
logging.debug(f"CLIENT_SECRET: {'*' * len(CLIENT_SECRET) if CLIENT_SECRET else None}")
logging.debug(f"TENANT_ID: {TENANT_ID}")
logging.debug(f"Server: {SERVER}")
logging.debug(f"Database Name: {DB_NAME}")
logging.debug(f"Tables: {TABLES}")
logging.debug(f"Save Path: {SAVE_PATH}")

def get_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        return None

def main():
    start_time = time.time()
    
    if len(sys.argv) > 1:
        # Running with command-line arguments
        parser = argparse.ArgumentParser(description='Fetch and save Power BI tables.')
        parser.add_argument('--server', help='Power BI server URL', default=SERVER)
        parser.add_argument('--db_name', help='Database name', default=DB_NAME)
        parser.add_argument('--tables', nargs='+', help='List of tables to download', default=TABLES)
        parser.add_argument('--save_path', help='Path where files will be saved', default=SAVE_PATH)

        # Filter out unrecognized arguments
        known_args, unknown_args = parser.parse_known_args()

        server = known_args.server
        db_name = known_args.db_name
        tables = known_args.tables
        save_path = known_args.save_path
    else:
        # Running interactively
        server = SERVER if SERVER else get_input('Enter Power BI server URL: ')
        db_name = DB_NAME if DB_NAME else get_input('Enter database name: ')
        tables = TABLES if TABLES else get_input('Enter tables to download (comma separated): ').split(',')
        save_path = SAVE_PATH if SAVE_PATH else get_input('Enter path where files will be saved: ')

    # Debug print statements to verify parameters
    logging.debug(f"Server: {server}")
    logging.debug(f"Database Name: {db_name}")
    logging.debug(f"Tables: {tables}")
    logging.debug(f"Save Path: {save_path}")

    try:
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path)

        fetch_tables(
            server=server,
            db_name=db_name,
            tables=tables,
            path=save_path,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            tenant_id=TENANT_ID
        )
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Script runtime: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
