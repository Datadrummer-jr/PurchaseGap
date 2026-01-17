from httpx import Client, HTTPError
import sys
import os
from dotenv import load_dotenv
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import my_functions as mf

load_dotenv()

API_EL_TOQUE = os.getenv('EL_TOQUE')

header = {
    "accept": "*/*",
    "Authorization": f"Bearer {API_EL_TOQUE}"
}

def toque(start: str,end: str):
    date = mf.days_range(start, end, False, False)
    urls = mf.days_range(start, end)
    with Client() as client:
        while date:
          try:
            url = f'https://rate.eltoque.com/v1/trmi?{urls[0]}'
            response = client.get(url=url, headers=header)
            response.raise_for_status()
            rate = response.json()
            lasts_rate = mf.read_json("../data/el_toque.json")
            lasts_rate[date[0]["date_from"]] = rate["rate"]
            mf.save_json( lasts_rate,"../data/el_toque.json")
            print(f'Se guardó el {date[0]["date_from"]}')
            date.pop(0)
            urls.pop(0)
            if not date:
               break
            sleep(10)
          except HTTPError:
             print('durmiendo por: ', date[0]["date_from"])
             sleep(60)
          
    return urls

if __name__ == "__main__":
    fecha_inicio = "2025-12-16"
    fecha_fin = "2025-12-31"
    toque(fecha_inicio, fecha_fin)
