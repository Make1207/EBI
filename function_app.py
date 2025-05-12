import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Fixed exchange rate (example: 1 EUR = 1.1 USD)
EXCHANGE_RATE = 1.1

@app.route(route="convert")
def convert(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Currency conversion function called.')

    # Get the "amount" parameter from query or body
    amount_str = req.params.get('Euro')
    if not amount_str:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        amount_str = req_body.get('Euro')

    # Try to convert and respond
    try:
        amount_eur = float(amount_str)
        amount_usd = amount_eur * EXCHANGE_RATE
        return func.HttpResponse(
            f"{amount_eur:.2f} EUR = {amount_usd:.2f} USD",
            status_code=200
        )
    except (TypeError, ValueError):
        return func.HttpResponse(
            "Please provide a valid numeric 'Euro' in the query string or JSON body.",
            status_code=400
        )
