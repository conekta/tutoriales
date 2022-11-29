import conekta
import uvicorn
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import RedirectResponse

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
    )
    url = order["checkout"]["url"]
    return RedirectResponse(url)


@router.get("/")
async def get_status():
    return {"Status": "OK",}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)