import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os

app = func.FunctionApp()

@app.route(route="ProcessDiet", auth_level=func.AuthLevel.ANONYMOUS)
def ProcessDiet(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing nutritional data from Azurite...")

    # Read the connection string from local.settings.json
    connect_str = os.getenv("AzureWebJobsStorage")

    # Create Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(
        connect_str,
        api_version="2023-11-03"
    )

    # Blob details
    container_name = "datasets"
    blob_name = "All_Diets.csv"

    # Download the CSV file
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    stream = blob_client.download_blob().readall()

    # Read CSV into DataFrame
    df = pd.read_csv(io.BytesIO(stream))

    # Fill missing values
    df[["Protein(g)", "Carbs(g)", "Fat(g)"]] = (
        df[["Protein(g)", "Carbs(g)", "Fat(g)"]]
        .fillna(df[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean())
    )

    # Calculate average macros by diet type
    avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()

    result = avg_macros.reset_index().to_dict(orient="records")

    # Save results locally
    os.makedirs("simulated_nosql", exist_ok=True)

    with open("simulated_nosql/results.json", "w") as f:
        json.dump(result, f, indent=2)

    # Return JSON response
    return func.HttpResponse(
        json.dumps(result, indent=2),
        mimetype="application/json",
        status_code=200
    )
