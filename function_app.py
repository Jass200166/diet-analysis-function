import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient
import pandas as pd
import json

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

    # Filter by diet type if provided
    if diet_type:
        df = df[df['Diet'].str.lower() == diet_type.lower()]

    # If no data found for that diet
    if df.empty:
        return func.HttpResponse(
            body=json.dumps({"message": "No records found for this diet."}),
            mimetype="application/json",
            status_code=200
        )

    # Real analysis
    result = {
        "total_records": len(df),
        "average_calories": float(df["Calories"].mean()),
        "average_protein": float(df["Protein"].mean()),
        "average_carbs": float(df["Carbs"].mean()),
        "average_fat": float(df["Fat"].mean()),
        "min_calories": float(df["Calories"].min()),
        "max_calories": float(df["Calories"].max())
    }

    return func.HttpResponse(
        body=json.dumps(result),
        mimetype="application/json",
        status_code=200
    )
