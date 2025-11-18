from httpx import AsyncClient, HTTPError
import anyio
from dotenv import load_dotenv
import os

load_dotenv()

API_EL_TOQUE = os.getenv('EL_TOQUE')

url =  'https://tasas.eltoque.com/v1/trmi?date_from=2022-10-27+00%3A00%3A01&date_to=2022-10-27+23%3A59%3A01'
header = {
    "accept": "*/*",
    "Authorization": f"Bearer {API_EL_TOQUE}"
}

async def toque():
  async with AsyncClient() as client:
            response = await client.get(url=url, headers=header)
            response.raise_for_status()
            print(response.json())
anyio.run(toque)

from urllib.parse import urlencode

params = {'nombre' : 'Joswald', 'edad': 20
    # "date_from": "2022-10-27 00:00:01",
    # "date_to": "2022-10-27 23:59:01"
}

# query_string = urlencode(params)
# print(query_string)
