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

def toque(inicio: str,fin: str):
    fechas = mf.intervalo_fechas(inicio, fin, False, False)
    urls = mf.intervalo_fechas(inicio, fin)
    with Client() as client:
        while fechas:
          try:
            url = f'https://tasas.eltoque.com/v1/trmi?{urls[0]}'
            response = client.get(url=url, headers=header)
            response.raise_for_status()
            tasas = response.json()
            tasas_actuales = mf.read_json("../data/el_toque.json")
            tasas_actuales[fechas[0]["date_from"]] = tasas["tasas"]
            mf.save_json( tasas_actuales,"../data/el_toque.json")
            print(f'Se guardó el {fechas[0]["date_from"]}')
            fechas.pop(0)
            urls.pop(0)
            if not fechas:
               break
            sleep(10)
          except HTTPError:
             print('durmiendo por: ', fechas[0]["date_from"])
             sleep(60)
          
    return urls

if __name__ == "__main__":
    fecha_inicio = "2025-12-16"
    fecha_fin = "2025-12-31"
    toque(fecha_inicio, fecha_fin)
