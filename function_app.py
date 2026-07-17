import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Diet analysis HTTP trigger function started.")

    # STEP 1 — Read JSON body safely
    try:
        data = req.get_json()
    except ValueError:
        data = {}

    # STEP 2 — Example input (you will replace this later)
    # If user sends: { "diet": "keto" }
    diet_type = data.get("diet", None)

    # STEP 3 — Placeholder logic (you will replace with real analysis)
    if diet_type:
        result = {
            "message": "Diet analysis completed",
            "diet_type": diet_type,
            "status": "success"
        }
        return func.HttpResponse(
            body=str(result),
            status_code=200
        )

    # STEP 4 — Default response
    return func.HttpResponse(
        "Send JSON like {\"diet\": \"keto\"} to run analysis.",
        status_code=200
    )
