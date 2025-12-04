import my_functions as mf
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import polars as pl
import sys

el_toque = mf.read_json('data/el_toque.json')
salarios = mf.read_json("data/escalas_salariales.json")
cities = mf.read_json("data/cities.json")
muni = mf.read_json("data/municipality_country.json")
abreviaturas = mf.read_json('data/abreviaturas.json')
city = ["HAB", "PRI", "ART", "MAY", "MTZ", "CFG", "VCL", "SSP", "CAV", "CAM", "LTU", "GRM", "HOL", "SCU", "GTM", "IJV"]
data = mf.read_json("data/pymes.json")
count_pymes = [len(mf.list_for_value(data, key='city', value= i.upper().replace(' ',''), second_key= "subject")) for i in cities ]
mipymes = mf.read_json("data/prices_pymes.json")
población_por_provincia =mf.read_json("data/población_cuba (2024).json")
canasta_básica = mf.read_json("data/canasta_básica.json")
qvapay = mf.read_json("data/qvapay.json")

def salary(file = salarios):
   for i in range(0,32):
     print(f"{i} | 44 horas: {file['44_horas'][i]} | 40 horas : {file['40_horas'][i]}")

def graph_coin():
  tasas = [el_toque[i['date_from']] for i in mf.intervalo_fechas("2025-01-01", "2025-11-30",False,False) if el_toque[i['date_from']] is not None]
  n = len(tasas)
  days = list(range(n))
  month = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre"]

  usd = [i["USD"] for i in tasas]
  euro = [i["ECU"] for i in tasas]
  mlc = [i["MLC"] for i in tasas]
  usd_oficial = [ 123.6 for _ in usd]

  inicios = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 302]
  
  plt.figure(figsize=(12, 6))
  plt.plot(days, usd, label='USD')
  plt.plot(days, euro, label = 'EURO')
  plt.plot(days, mlc, label = 'MLC')
  # plt.plot(days[0:304], usd_oficial[0:304], label='USD en Cadeca')
  plt.xticks(inicios, month, rotation=0)
  plt.title('Comparación del comportamiento del USD, el EURO y el MLC entre enero y noviembre de 2025.')
  plt.legend()
  plt.show()

def bar_pymes():      
  count_city = np.arange(len(count_pymes))
  plt.figure(figsize=(14, 6))
  plt.bar(count_city, count_pymes)
  plt.xticks(count_city,city, rotation=0)
  plt.show()


def compra_máxima(prices: list[int|float], escala : int) -> int:
    matriz = [-sys.maxsize] * (escala+1)
    matriz[0] = 0
    for i in prices:
        for j in range(escala, i - 1, -1):
            matriz[j] = max(matriz[j], matriz[j - i] + 1)
    return int(max(matriz))
      
def compra_por_escala(escala: int):
   máximos = [compra_máxima(mf.dict_num_values(mipymes[i]['products']), escala) for i in mipymes if mipymes[i]["sales_category"] == "minorista"]
   return  int(np.median(máximos))

def max_bar():
  max_products = [compra_por_escala(s) for s in salarios['44_horas']]
  count_escalas = np.arange(len(salarios['44_horas']))
  plt.figure(figsize=(16, 10))
  plt.barh(count_escalas, max_products,  color= "yellow")
  plt.yticks(count_escalas, salarios['44_horas'], rotation=0)
  plt.title('Mediana de la cantidad máxima de productos que se pueden adquirir en un establecimiento de comercio según escala salarial de 44 horas laborales.')
  plt.show()

población  = [ población_por_provincia[abreviaturas[i]]["total"] for i in city]

for_hab = [ int(población[i] // count_pymes[i]) for i in range(len(población))]

provincias = [abreviaturas[i] for i in city]

types = [mf.list_for_value(data,'city',i , "subject") for i in cities]
mpmp =  [mf.first_count(i, 'MIPYME PRIVADA') for i in types]
mpme =  [mf.first_count(i, 'MIPYME ESTATAL') for i in types]
cna =   mf.sum_row([[mf.first_count(i, 'COOPERATIVA NO AGROPECUARIA') for i in types], [mf.first_count(i, 'CNA') for i in types]])
mipymes_indefinidas = [mf.del_space(i).count('MIPYME') for i in types]

def ausent_detect(lista:list[str]):
  for i in lista:
    if 'MIPYME PRIVADA'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
      'MIPYME ESTATAL'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
      'MIPYME'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
      'CNA'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
      'COOPERATIVA NO AGROPECUARIA'.upper().replace(' ','') not in str(i).upper().replace(' ',''):
       return i
  return 'ok'

df_for_type_and_hab = pd.DataFrame({
   "Provincias": provincias + ['Cuba'],
   "Mipymes Privadas": mpmp + [sum(mpmp)], 
   "Mipymes Estatales": mpme + [sum(mpme)] ,
   "Mipymes Indefinidas":  mipymes_indefinidas + [sum(mipymes_indefinidas)], 
   "CNA": cna + [sum(cna)],
   "Total": mf.sum_row([mpmp,mpme,cna,mipymes_indefinidas]) + [sum(mf.sum_row([mpmp,mpme,cna,mipymes_indefinidas]))], 
   "Cantidad de actores económicos por habitante": for_hab + [int(población_por_provincia["Cuba"]["total"] // sum(count_pymes))] })

percent = (len(mipymes) * 100) / len(data)

text_pyme = f"Para contar esta historia se obtuvieron datos de {len(mipymes)} actores económicos de diferentes dominios que  \
representan sólo un { f"{round(percent,2)} %"} del total de los creados\n desde 2021, pero con planes  \
de que este porciento alcance el 30 % en un futuro no muy lejano."

pymes_keys = [k for k in mipymes]
canasta_keys = [k for k in canasta_básica]

def price_media(product: str):
  return np.mean(mf.aplanar_lista([mf.dict_num_values(mf.search_keys(mipymes[a]["products"], product)) for a in pymes_keys ])), np.mean(mf.aplanar_lista(mf.dict_num_values(mf.search_keys(canasta_básica, product))))

pymes_arroz ,canasta_arroz = price_media("arroz")

pymes_pollo ,canasta_pollo =  price_media("pollo")

pymes_azúcar, canasta_azúcar = price_media("azúcar")

pymes_frijoles, canasta_frijoles = price_media("frijoles")

pymes_aceite, canasta_aceite = price_media("aceite")

pymes_picadillo, canasta_picadillo = price_media("picadillo")

pymes_mortadella, canasta_mortadella = price_media("mortadella")

pymes_café, canasta_café = price_media("café")

pymes_pan, canasta_pan = price_media("pan")

pymes_leche, canasta_leche = price_media("leche")

pymes_yogurt, canasta_yogurt = price_media("yogurt")

pymes_pescado, canasta_pescado = price_media("pescado")

def bar_canasta_vs_pymes():
    products = ["Mipymes", "Canasta Básica"]
    fig = make_subplots(rows=6, cols=2,
               specs=[[{"type": "pie"}, {"type": "pie"}],
                      [{"type": "pie"}, {"type": "pie"}],
                      [{"type": "pie"}, {"type": "pie"}],
                      [{"type": "pie"}, {"type": "pie"}],
                      [{"type": "pie"}, {"type": "pie"}],
                      [{"type": "pie"}, {"type": "pie"}]], 
                      subplot_titles= ["Arroz", "Pollo", "Azúcar", "Frijoles", "Aceite", "Picadillo",
              "Mortadella", "Café", "Pan", "Peche","Yogurt" , "Pescado"])
    fig.add_trace(go.Pie(labels=products,values=[pymes_arroz, canasta_arroz]), 1, 1)
    fig.add_trace(go.Pie(labels=products,values=[pymes_pollo, canasta_pollo]), 1, 2)
    fig.add_trace(go.Pie(labels=products,values=[pymes_arroz, canasta_arroz]), 2, 1)
    fig.add_trace(go.Pie(labels=products,values=[pymes_pollo, canasta_pollo]), 2, 2)
    fig.add_trace(go.Pie(labels=products,values=[pymes_arroz, canasta_arroz]), 3, 1)
    fig.add_trace(go.Pie(labels=products,values=[pymes_pollo, canasta_pollo]), 3, 2)
    fig.add_trace(go.Pie(labels=products,values=[pymes_arroz, canasta_arroz]), 4, 1)
    fig.add_trace(go.Pie(labels=products,values=[pymes_pollo, canasta_pollo]), 4, 2)
    fig.add_trace(go.Pie(labels=products,values=[pymes_arroz, canasta_arroz]), 5, 1)
    fig.add_trace(go.Pie(labels=products,values=[pymes_pollo, canasta_pollo]), 5, 2)
    fig.add_trace(go.Pie(labels=products,values=[pymes_arroz, canasta_arroz]), 6, 1)
    fig.add_trace(go.Pie(labels=products,values=[pymes_pollo, canasta_pollo]), 6, 2)
   
    fig.update_layout(height=800, barmode='group', xaxis_tickangle=-45, title="Gráficas comparativas del costo de los principales productos de la canasta básica contra los productos vendidos por mipymes")
    fig.show()

def qvapay_vs_el_toque():
  fechas = [fecha['date_from'] for fecha in mf.intervalo_fechas('2025-11-24','2025-11-30', False, False)]
  usd_qvapay = []
  for fecha in fechas:
    offers = []
    for offer in qvapay:
      if qvapay[offer]["date"][:10] == fecha and qvapay[offer]["coin"] == "CUP":
         offers.append(qvapay[offer]["price"])  
    usd_qvapay.append(offers)
  medias = [len(m) for m in usd_qvapay]
  return medias

print(qvapay_vs_el_toque())




