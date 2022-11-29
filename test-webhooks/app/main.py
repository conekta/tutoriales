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