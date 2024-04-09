from fastapi import FastAPI
from middlewares import CustomHeaderMiddleware
from src.routes import contacts

import uvicorn

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.add_middleware(CustomHeaderMiddleware)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)