from fastapi import FastAPI, Response
import uvicorn
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

@app.get("/")
def message(response: Response):
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    uvicorn.run('main:app', host=host, port=port)