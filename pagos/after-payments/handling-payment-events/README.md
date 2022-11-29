# Probar localmente los Webhooks con Ngrok

## ¿Por qué utilizar ngrok para las pruebas locales?

Conekta requiere que tus webhooks sean accesibles públicamente para que puedan ser utilizados con nuestros servicios. Esto puede dificultar las pruebas en entornos locales, ya que la mayoría de los ordenadores tienen algunos routers/firewalls que impiden que esto tenga lugar sin NAT.

Una herramienta que facilita las pruebas locales es ngrok, un servicio que proporciona una URL HTTPS que tuneliza las peticiones a su aplicación web que se ejecuta localmente en un puerto.

## Cómo utilizar ngrok

Una vez que tengas ngrok instalado, puedes ejecutar un comando como `ngrok http 8000` dependiendo del puerto que quieras utilizar. En la pestaña de reenvío, verás una URL de ngrok que apunta a tu localhost en el puerto que has especificado.

Usaremos esta URL para dar acceso a Conekta a tu aplicación web mientras la ventana de ngrok se esté ejecutando.

```bash
ngrok

Try our new native Go library: https://github.com/ngrok/ngrok-go

Session Status                online
Session Expires               1 hour, 59 minutes
Terms of Service              https://ngrok.com/tos
Version                       3.1.0
Region                        Europe (eu)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://920c-81-35-24-51.eu.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

A continuación debemos ejecutar ngrok y nuestro script como webhook al mismo tiempo para poder aceptar la solicitud de conekta cuando se genere un evento como consecuencia de una transición en el ciclo de pago.

Ejecuta el siguiente frangmento de codigo para probar:

```python
import uvicorn
from fastapi import FastAPI, Request, APIRouter

router = APIRouter()
app = FastAPI()

@router.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    return body


@router.get("/")
async def get_status():
    return {"Status": "OK",}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Para la url de prueba de webhook, se combinaría la ruta `/webhook` con la url de ngrok. La url del webhook resultante sería algo así como https://920c-81-35-24-51.eu.ngrok.io/webhook.

## Registrar webhook de prueba en Conekta.

```bash
curl --location --request POST 'https://api.conekta.io/webhooks' \
--header 'Accept: application/vnd.conekta-v2.0.0+json' \
--header 'Accept-Language: es' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer key_KSdfawe..' \
--data-raw '{
	"url": "https://920c-81-35-24-51.eu.ngrok.io/webhook",
	"synchronous": false
}'
```

```json
{
    "id":"63864a6b2e2ae0001841ef1c",
    "synchronous":false,
    "production_enabled":false,
    "development_enabled":true
    "url":"https://920c-81-35-24-51.eu.ngrok.io/webhook","status":"intermittent_errors",
    "subscribed_events":[
        "charge.created",
        "charge.paid",
        "charge.under_fraud_review",
        "charge.fraudulent",
        "charge.refunded",
        "charge.preauthorized",
        "charge.declined",
        "charge.canceled",
        "charge.reversed",
        "charge.pending_confirmation",
        "charge.expired",
        "customer.created",
        "customer.updated",
        "customer.deleted",
        "webhook.created",
        "webhook.updated",
        "webhook.deleted",
        "charge.chargeback.created",
        "charge.chargeback.updated",
        "charge.chargeback.under_review",
        "charge.chargeback.lost",
        "charge.chargeback.won",
        "payout.created",
        "payout.retrying",
        "payout.paid_out",
        "payout.failed",
        "plan.created",
        "plan.updated",
        "plan.deleted",
        "subscription.created",
        "subscription.paused",
        "subscription.resumed",
        "subscription.canceled",
        "subscription.expired",
        "subscription.updated",
        "subscription.paid",
        "subscription.payment_failed",
        "payee.created",
        "payee.updated",
        "payee.deleted",
        "payee.payout_method.created",
        "payee.payout_method.updated",
        "payee.payout_method.deleted",
        "charge.score_updated",
        "receipt.created",
        "order.canceled",
        "order.charged_back",
        "order.created",
        "order.expired",
        "order.fraudulent",
        "order.under_fraud_review",
        "order.paid",
        "order.partially_refunded",
        "order.pending_payment",
        "order.pre_authorized",
        "order.refunded",
        "order.updated",
        "order.voided",
        "order.declined",
        "cashout.canceled",
        "cashout.confirmed",
        "webhook_ping",
        "customer.payment_source.card.blocked"
    ]
}
```

## Borrar webhook de prueba en Conekta

```bash
curl --location --request DELETE 'https://api.conekta.io/webhooks/63864a6b2e2ae0001841ef1c' \
--header 'Accept: application/vnd.conekta-v2.0.0+json' \
--header 'Accept-Language: es' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer key_KSdfawe...' \
```