import unittest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


class Test_FastAPI(unittest.TestCase):

    # Lage en test for å se om en kan få ut firerisks
    def Test_get_fire_risk():
        pass

    # Lage en test for å lage en fil
    def Test_make_file():
        pass
    
    # Lage en test for å se om vi kan fastapi
    def Test_open_fast_api():
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}