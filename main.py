from fastapi import FastAPI, Response
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

@app.get("/")
def message(response: Response):
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    uvicorn.run('main:app', host=host, port=port)