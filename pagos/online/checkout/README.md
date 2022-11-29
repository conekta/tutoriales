# Cobra con Conekta Checkout

## Configurar Conekta.
[Registrate](https://panel.conekta.com) en Conekta y genera tus llaves secretas para autenticar tus API Requests. Para el desarrollo de tus servicios necesitaras la llave privada

## Redirige a tu cliente al Checkout de Conekta

Agrega un boton de checkout en tu sitio web que ejecute un llamado al API de Conekta desde tu servidor para crear una Order.

```html
<html>
	<head>
		<title>Buy cool new product</title>
	</head>   
	<body>
		<form action="/create-checkout-session" method="POST">
			<button type="submit">Pagar con Conekta</button>
		</form>   
	</body>
</html>`
```

El objeto Order representa la intención de compra de tu cliente. Incluye todos los detalles relacionados a ella, como metodos de pago, información de envio, lista de productos a comprar, cargos, descuentos, impuesto, etc.

La Order requiere información del cliente (Objeto Customer). El objeto Customer representa un cliente de tu negocio. Permite crear cargos recurrentes y hacer un seguimiento de los pagos que pertenecen al mismo.

Puedes crear un nuevo Customer o reutilizar la información de un Customer creado previamente.

Luego de crear una orden, redirige a tu cliente a la URL devuelta en la respuesta de la API de ordenes.

```python
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
```

Prueba tu integración iniciando tu servidor web (`http://0.0.0.0:8000`) y ejecutando el siguiente comando

```bash
curl -X POST -is "http://0.0.0.0:8000/checkout" -d ""
```

```bash
HTTP/1.1 307 Temporary Redirect
server: uvicorn
location: https://pay.conekta.com/checkout/c8c044b3b5084345baf616e4c811e021
...
```

## Capturar eventos del pago.

Conekta permite automatizar acciones enviando eventos en respuesta a las transiciones que se producen en el flujo de pagos. Para recibir estos eventos y ejecutar acciones siga la guía de webhook.

Se recomienda capturar los siguientes eventos cuando cobre pagos con el checkout:

|Evento|Descripción|
|---|---|
|order.paid |Enviado cuando un cliente completa un pago de forma exitosa|
|order.pending_payment|Enviado cuando una orden es creada pero continua pendiente de pagar|
|order.declined|Enviado cuando el pago de una orden es declinado|

Al capturar estos eventos podras tomar acciones post-venta como:
* Ejecutar un flujo de logistica.
* Actualizar tus bases de datos de ordenes.
* Actualizar tus sistemas contables.

# Pruebas en local