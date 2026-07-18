import logging
import azure.functions as func
import os
from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Diet analysis HTTP trigger started.")

    try:
        connect_str = os.getenv("AzureWebJobsStorage")
        blob_service = BlobServiceClient.from_connection_string(connect_str)

        container_name = "dietdata"
        blob_name = "All_Diets.csv"

        blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
        csv_bytes = blob_client.download_blob().readall()

        df = pd.read_csv(BytesIO(csv_bytes))
        summary = df.describe(include="all").to_dict()

        return func.HttpResponse(
            json.dumps(summary, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
