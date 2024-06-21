

import requests
import pandas as pd
import httpx
from celery import shared_task

class APIConnector:
    def __init__(self,ip,token):
        self.base_url = f'http://{ip}:3005/api/consulta'
        self.token = token
        
    def send_get_json(self, endpoint, params=None):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers,params = params)
        if response.status_code == 200:
            print("La solicitud fue exitosa.")
        else:
            print("La solicitud no fue exitosa. Código de estado:", response.status_code)
        return response.json()
    #@shared_task
    def send_get_dataframe(self, endpoint, params=None):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers,params = params)
        obj = response.json()
        obj_ = obj['objeto']
        return pd.DataFrame(obj_)
    

async def fetch_data_from_api(ip = None, token = None,sp = None, params = None):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{ip}:3005/api/consulta/{sp}", headers=headers, params = params, timeout=100.0)
        response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es 2xx
        obj = response.json()
        obj_ = obj['objeto']
        return obj_



