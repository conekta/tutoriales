from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseSettings
import conekta

class Settings(BaseSettings):
    conekta_api_key: str = ""

settings = Settings()
router = APIRouter()
app = FastAPI()
conekta.api_key = settings.conekta_api_key
conekta.locale = "es"

@router.get("/checkout")
async def create_checkout(request: Request):
    payload = {
		"currency": "MXN",
		"customer_info": {
            "customer_id": "cus_2shKUY6Rvwg1nSEiq"
		},
		"line_items": [
			{
				"name": "Nintendo Switch OLED",
				"unit_price": 15000000,
				"quantity": 3
			}
		],
		"checkout": {
			"type": "HostedPayment",
			"allowed_payment_methods": ["cash", "card", "bank_transfer"],
			"success_url": "https://www.github.com/macuartin",
			"failure_url": "https://www.twitter.com/macuartin",
		},
	}

    order = conekta.Order.create(payload)
    url = order["checkout"]["url"]
    return RedirectResponse(url)


@router.get("/ping")
async def get_ping():
    return {
        "Status": "OK",
    }

@app.get("/success", response_class=HTMLResponse)
async def get_success_page():
    html_content = """
    <html>
        <head>
            <title>Success Page</title>
        </head>
        <body>
            <h1>Gracias por tu pago</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/cancel", response_class=HTMLResponse)
async def get_error_page():
    html_content = """
    <html>
        <head>
            <title>Error Page</title>
        </head>
        <body>
            <h1>Algo salio mal</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/", response_class=HTMLResponse)
async def get_store():
    html_content = """
    <html>
        <head>
            <title>Buy cool new product</title>
        </head>   
        <body>
            <form action="http://0.0.0.0:8000/checkout" method="get">
                <button type="submit">Pagar con Conekta</button>
            </form>   
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

app.include_router(router)