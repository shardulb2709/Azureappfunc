import logging
import os
import psycopg2
from azure.identity import DefaultAzureCredential

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # PostgreSQL connection details
    server_name = "pgfs3n.postgres.database.azure.com"
    database_name = "postgres"
    username = "shardul1"  # Managed Identity name

    try:
        # Get an access token using Managed Identity
        credential = DefaultAzureCredential()
        token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default")

        # Establish a connection to PostgreSQL
        conn = psycopg2.connect(
            host=server_name,
            database=database_name,
            user=username,
            password=token.token,
            sslmode="require"
        )

        # Execute a sample query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()

        return func.HttpResponse(f"Connected to PostgreSQL. Database version: {db_version[0]}", status_code=200)
        print("Logged in")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Failed to connect to PostgreSQL: {str(e)}", status_code=500)