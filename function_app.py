import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient
import pandas as pd
import json
from io import BytesIO

# Azure Function App (anonymous access)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ---------------------------------------------------------
# HTTP Trigger Route (THIS FIXES YOUR 404 ERROR)
# ---------------------------------------------------------
@app.function_name(name="ProcessDiet")
@app.route(route="ProcessDiet", auth_level=func.AuthLevel.ANONYMOUS)
def process_diet(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Diet analysis HTTP trigger started.")

    try:
        # ---------------------------------------------------------
        # Connect to Azure Storage using Function App's connection string
        # ---------------------------------------------------------
        connect_str = os.getenv("AzureWebJobsStorage")
        blob_service = BlobServiceClient.from_connection_string(connect_str)

        # Your Azure Storage container + blob
        container_name = "dietdata"
        blob_name = "All_Diets.csv"

        blob_client = blob_service.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        # ---------------------------------------------------------
        # Read CSV file from Azure Blob Storage
        # ---------------------------------------------------------
        csv_bytes = blob_client.download_blob().readall()
        df = pd.read_csv(BytesIO(csv_bytes))

        # ---------------------------------------------------------
        # Generate summary statistics
        # ---------------------------------------------------------
        summary = df.describe(include="all").to_dict()

        # ---------------------------------------------------------
        # Return JSON response
        # ---------------------------------------------------------
        return func.HttpResponse(
            json.dumps(summary, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            f"Error processing diet data: {str(e)}",
            status_code=500
        )
