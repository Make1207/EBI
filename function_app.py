import logging
import azure.functions as func
import json

EMAIL_MAP = {
    "Welcome": "Welcome-Gruppe@mailprovider.com",
    "First-Level": "First-Level-Gruppe@mailprovider.com",
    "Second-Level": "Second-Level-Gruppe@mailprovider.com",
    "Unknown": "Support-Gruppe@mailprovider.com"
}

app = func.FunctionApp()

def classify_email(body: str):
    body = body.lower()
    if any(word in body for word in ["willkommen", "neu", "starten", "einführung"]):
        return "Welcome"
    elif any(word in body for word in ["fehler", "problem", "hilfe", "nicht funktionieren"]):
        return "First-Level"
    elif any(word in body for word in ["dringend", "datenverlust", "sicherheitsproblem", "eskalation"]):
        return "Second-Level"
    else:
        return "Unknown"

@app.function_name(name="ClassifyEmail")
@app.route(route="classify", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('E-Mail wird klassifiziert.')

    # Überprüfen, ob der "body"-Parameter in der URL enthalten ist
    body_text = req.params.get('body')
    if not body_text:
        try:
            data = req.get_json()
            body_text = data.get("body", "")
        except Exception:
            return func.HttpResponse("Missing or invalid 'body' parameter.", status_code=400)

    # Klassifikation der E-Mail
    classification = classify_email(body_text)
    
    # E-Mail-Adresse anhand der Klassifikation ermitteln
    email_address = EMAIL_MAP.get(classification, "Support-Gruppe@mailprovider.com")

    # Rückgabe der Klassifikation und der E-Mail-Adresse als JSON
    response = {
        "classification": classification,
        "email": email_address
    }

    return func.HttpResponse(
        json.dumps(response),
        mimetype="application/json"
    )
