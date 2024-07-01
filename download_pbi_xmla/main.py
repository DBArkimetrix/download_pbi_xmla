import argparse
import polars as pl
import msal
import os
from download_pbi_xmla.ssas_api import set_conn_string, get_DAX

# Configuration for MSAL
CLIENT_ID = "your_client_id"  # Replace with your actual client ID
TENANT_ID = "your_tenant_id"  # Replace with your actual tenant ID
AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://analysis.windows.net/powerbi/api/.default"]

# Function to fetch and save table data
def fetch_and_save_table(table_name, conn_str, file_name):
    query = f'EVALUATE {table_name}'
    try:
        df = get_DAX(conn_str, query)
        pl_df = pl.DataFrame(df)
        print(f"Table '{table_name}' fetched successfully!")
        pl_df.write_parquet(file_name)
        print(f"Table '{table_name}' saved to {file_name}")
    except Exception as e:
        print(f"Failed to fetch or save table '{table_name}'.")
        print(str(e))

# Function to get the access token
def get_access_token():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)
    accounts = app.get_accounts()
    
    if accounts:
        # Attempt silent token acquisition first
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        result = None

    if not result:
        # Fallback to device code flow if silent token acquisition fails
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise ValueError("Failed to create device flow")
        
        print(flow["message"])

        result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise ValueError("Failed to acquire token")

# New function to fetch tables
def fetch_tables(server, db_name, username, password, tables, path, use_mfa=True):
    if use_mfa:
        token = get_access_token()
        conn_str = set_conn_string(server, db_name, username, password) + f";Token={token}"
    else:
        conn_str = set_conn_string(server, db_name, username, password)
    
    for table in tables:
        file_path = os.path.join(path, f"{table}.parquet")
        fetch_and_save_table(table, conn_str, file_path)

# Main function for CLI usage
def main():
    parser = argparse.ArgumentParser(description='Fetch and save Power BI tables.')
    parser.add_argument('--server', required=True, help='Power BI server URL')
    parser.add_argument('--db_name', required=True, help='Database name')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', required=True, help='Password')
    parser.add_argument('--tables', required=True, nargs='+', help='List of tables to download')
    parser.add_argument('--path', required=True, help='Path where parquet files will be saved')
    parser.add_argument('--use_mfa', action='store_true', help='Use MFA for authentication')
    args = parser.parse_args()

    try:
        fetch_tables(args.server, args.db_name, args.username, args.password, args.tables, args.path, args.use_mfa)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
