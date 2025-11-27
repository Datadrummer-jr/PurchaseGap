import my_functions as mf
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import xlrd
import numpy as np

salarios = mf.read_json("data/escalas_salariales.json")
cities = mf.read_json("data/cities.json")
muni = mf.read_json("data/municipality_country.json")

def salary(file = salarios):
   for i in range(0,32):
     print(f"{i} | 44 horas: {file['44_horas'][i]} | 40 horas : {file['40_horas'][i]}")

def graph_coin():
  tasas = mf.read_json('data/el_toque.json')

  days = [i for i in range(304)]
  month = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre"]

  usd = [tasas[i]["USD"] for i in tasas]
  euro = [tasas[i]["ECU"] for i in tasas]
  usd_oficial = [ 123.6 for _ in usd]

  # Índices del inicio de cada mes (día 0 = 1 de enero)
  inicios = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273]
  
  plt.figure(figsize=(12, 6))
  plt.plot(days[0:304], usd[0:304], label='USD')
  plt.plot(days[0:304], euro[0:304], label = 'EURO')
  # plt.plot(days[0:304], usd_oficial[0:304], label='USD en cadeca')
  plt.xticks(inicios, month, rotation=0)
  plt.title('Comparación del comportamiento del USD y el EURO entre enero y octubre de 2025.')
  plt.legend()
  plt.show()

def bar_pymes():
  data = mf.read_json("data/pymes.json")
  city = [len(mf.list_for_value(data, key='city', value= i.upper().replace(' ',''), second_key='type')) for i in cities ]
  presentes = [ data[i]['city'] for i in data ]
  faltantes = [i for i in data if data[i]['city'].upper() not in [ i.upper() for i in cities] ]
  subject = None
  # provincias =  mf.list_for_value(data,'city') 
  # mpmp = subject.count('MIPYME PRIVADA')
  # mpme =  subject.count('MIPYME ESTATAL')
  # cna =  subject.count('COOPERATIVA NO AGROPECUARIA') +  subject.count('CNA')
  # city = [provincias.count(i) for i in cities]
  # count_subject = np.arange(len(city))
  # fig, ax = plt.subplots()
  return city



