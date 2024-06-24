import argparse
import polars as pl
import msal
import os
from download_pbi_xmla.ssas_api import set_conn_string, get_DAX

# Configuration for MSAL
CLIENT_ID = "your_client_id"
TENANT_ID = "your_tenant_id"
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
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        result = None

    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise ValueError("Failed to create device flow")
        
        print(flow["message"])

        result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise ValueError("Failed to acquire token")

# Main function
def main():
    parser = argparse.ArgumentParser(description='Fetch and save Power BI tables.')
    parser.add_argument('--server', required=True, help='Power BI server URL')
    parser.add_argument('--db_name', required=True, help='Database name')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', required=True, help='Password')
    parser.add_argument('--tables', required=True, nargs='+', help='List of tables to download')
    parser.add_argument('--path', required=True, help='Path where parquet files will be saved')
    args = parser.parse_args()

    token = get_access_token()
    conn_str = f"Provider=MSOLAP;Data Source={args.server};Initial Catalog={args.db_name};User ID={args.username};Password={args.password};Persist Security Info=True;Impersonation Level=Impersonate;Token={token}"
    
    for table in args.tables:
        file_path = os.path.join(args.path, f"{table}.parquet")
        fetch_and_save_table(table, conn_str, file_path)

if __name__ == "__main__":
    main()
