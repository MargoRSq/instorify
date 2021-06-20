from fastapi import FastAPI
import requests


app = FastAPI(title='api')

@app.get("/")
async def root():
    r = requests.get('http://127.0.0.1:8000/docs')
    return r.headers