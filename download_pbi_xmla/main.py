import polars as pl
import msal
import os
from download_pbi_xmla.ssas_api import set_conn_string, get_DAX

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

def get_access_token(client_id, client_secret, tenant_id):
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret
    )
    scopes = ["https://analysis.windows.net/powerbi/api/.default"]
    result = app.acquire_token_for_client(scopes=scopes)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise ValueError("Failed to acquire token")

def fetch_tables(server, db_name, username, password, tables, path, client_id, client_secret, tenant_id, use_mfa=False):
    if use_mfa:
        token = get_access_token(client_id, client_secret, tenant_id)
        conn_str = set_conn_string(server, db_name, username, password) + f";Bearer {token}"
    else:
        conn_str = set_conn_string(server, db_name, username, password)
    
    for table in tables:
        file_path = os.path.join(path, f"{table}.parquet")
        fetch_and_save_table(table, conn_str, file_path)
