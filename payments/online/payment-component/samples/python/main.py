import conekta
import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request, APIRouter
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "public"))

router = APIRouter()
app = FastAPI()
conekta.api_key = ""
conekta.locale = "es"

@router.post("/checkout")
async def create_checkout(request: Request):

    customer = conekta.Customer.create(
        {
            "name": "Miguel Cuartin",
            "email": "miguel.cuartin@conekta.com"
        }
    )

    order = conekta.Order.create(
        {
            "currency": "MXN",
            "customer_info": {
                "customer_id": customer["id"]
            },
            "line_items": [
                {
                    "name": "Nintendo Switch OLED",
                    "unit_price": 9000000,
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
    )
    checkout_id = order["checkout"]["id"]
    return templates.TemplateResponse("index.html", {"request": request, "checkout_id": checkout_id})


@router.get("/")
async def return_ecommerce(request: Request):
    return templates.TemplateResponse("button.html", {"request": request})

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)