import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient
import pandas as pd

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Diet analysis HTTP trigger started.")

    # Read JSON input
    try:
        data = req.get_json()
    except ValueError:
        data = {}

    diet_type = data.get("diet", None)

    # Connect to Blob Storage using environment variable
    connect_str = os.getenv("AzureWebJobsStorage")
    blob_service = BlobServiceClient.from_connection_string(connect_str)

    # Container + file name
    container_name = "dietdata"
    blob_name = "All_Diets.csv"

    # Download CSV
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
    csv_data = blob_client.download_blob().readall()

    # Load into pandas
    df = pd.read_csv(pd.io.common.BytesIO(csv_data))

    # Placeholder analysis
    summary = df.describe().to_dict()

    return func.HttpResponse(
        body=str(summary),
        status_code=200
    )
