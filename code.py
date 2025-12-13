import my_functions as mf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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


última_tasa = mf.dict_for_index(el_toque,-1)

mipymes_cup = {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "CUP"}
mipymes_usd =  {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "USD"}
mipymes_eur = {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "EUR"}

def salary(file = salarios):
   for i in range(0,32):
     print(f"{i} | 44 horas: {file['44_horas'][i]} | 40 horas : {file['40_horas'][i]}")

def graph_coin():
  tasas = [el_toque[i['date_from']] for i in mf.intervalo_fechas("2025-01-01", "2025-12-10",False,False) if el_toque[i['date_from']] is not None]
  n = len(tasas)
  days = list(range(n))
  month = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

  usd = [i["USD"] for i in tasas]
  euro = [i["ECU"] for i in tasas]
  mlc = [i["MLC"] for i in tasas]

  inicios = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

  fig = go.Figure(data=[
  go.Scatter(x=days, y=usd, mode="lines", name= 'USD'),
  go.Scatter(x=days, y=euro, mode="lines", name= 'EURO'),
  go.Scatter(x=days, y=mlc, mode="lines", name= 'MLC')
  ]
  )

  fig.update_xaxes(
   tickvals=inicios,  
    ticktext=month,  
    tickangle=0
  )
  fig.update_layout(title='Comparación del comportamiento del USD, el EURO y el MLC entre enero y 10 de diciembre de 2025.')
  fig.show()
  

# def bar_pymes():      
#   fig = go.Figure(data=go.Bar(
#      x= city,
#      y = count_pymes
#   ))
#   fig.update_layout(title= "Comparación de la cantidad de actores económicos creados desde 2021 por provincia.")
#   fig.show()
      
def compra_por_escala(escala: int):
   máximos = [mf.max_objects([int(i*última_tasa["ECU"])for i in mf.dict_num_values(mipymes[i]['products'])], escala) 
              if  mipymes[i]["currency"] == "EUR" 
              else
              mf.max_objects([int(i*última_tasa["USD"])for i in mf.dict_num_values(mipymes[i]['products'])], escala) 
              if mipymes[i]["currency"] == "USD"
              else mf.max_objects([int(i) for i in mf.dict_num_values(mipymes[i]['products'])], escala) 
              for i in mipymes if mipymes[i]["sales_category"] == "minorista"]
   return  int(mf.median(máximos))

def max_bar():
  max_products = [compra_por_escala(s) for s in salarios['44_horas']]
  count_escalas = list(range(len(salarios['44_horas'])))
  fig = go.Figure(data=[
     go.Bar(x= max_products, y= count_escalas, orientation="h", marker=dict(color="yellow"))
  ])
  fig.update_yaxes(
    tickvals= count_escalas,  
    ticktext= salarios['44_horas'],  
    tickangle=0
  )
  fig.update_layout(height=700, title='Mediana de la cantidad máxima de productos que se pueden adquirir en un establecimiento de comercio según escala salarial.')
  fig.show()

# población  = [ población_por_provincia[abreviaturas[i]]["total"] for i in city]

# for_hab = [ int(población[i] // count_pymes[i]) for i in range(len(población))]

# provincias = [abreviaturas[i] for i in city]

# types = [mf.list_for_value(data,'city',i , "subject") for i in cities]
# mpmp =  [mf.first_count(i, 'MIPYME PRIVADA') for i in types]
# mpme =  [mf.first_count(i, 'MIPYME ESTATAL') for i in types]
# cna =   mf.sum_rows([[mf.first_count(i, 'COOPERATIVA NO AGROPECUARIA') for i in types], [mf.first_count(i, 'CNA') for i in types]])
# mipymes_indefinidas = [mf.del_space(i).count('MIPYME') for i in types]

# def ausent_detect(lista:list[str]):
#   for i in lista:
#     if 'MIPYME PRIVADA'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
#       'MIPYME ESTATAL'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
#       'MIPYME'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
#       'CNA'.upper().replace(' ','') not in str(i).upper().replace(' ','') and \
#       'COOPERATIVA NO AGROPECUARIA'.upper().replace(' ','') not in str(i).upper().replace(' ',''):
#        return i
#   return 'ok'

# df_for_type_and_hab = pl.DataFrame({
#    "Provincias": provincias + ['Cuba'],
#    "Mipymes Privadas": mpmp + [sum(mpmp)], 
#    "Mipymes Estatales": mpme + [sum(mpme)] ,
#    "Mipymes Indefinidas":  mipymes_indefinidas + [sum(mipymes_indefinidas)], 
#    "CNA": cna + [sum(cna)],
#    "Total": mf.sum_rows([mpmp,mpme,cna,mipymes_indefinidas]) + [sum(mf.sum_rows([mpmp,mpme,cna,mipymes_indefinidas]))], 
#    "Cantidad de actores económicos por habitante": for_hab + [int(población_por_provincia["Cuba"]["total"] // sum(count_pymes))] })


def price_media(product: str):
  canasta =  mf.aplanar_lista(mf.dict_num_values(mf.search_keys(canasta_básica, product)))
  usd = list(map(lambda x: x* última_tasa["USD"],  mf.aplanar_lista([mf.dict_num_values(mf.search_keys(mipymes_usd[a]["products"], product)) for a in mipymes_usd ])))
  eur = list(map(lambda x: x*última_tasa['ECU'], mf.aplanar_lista([mf.dict_num_values(mf.search_keys(mipymes_eur[a]["products"], product)) for a in mipymes_eur ])))
  cup= mf.aplanar_lista([mf.dict_num_values(mf.search_keys(mipymes_cup[a]["products"], product)) for a in mipymes_cup])
  return mf.mean(cup+usd+eur) , mf.mean(canasta)

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
    products = ["arroz", "pollo" , "azúcar", "frijoles", "aceite", "picadillo", "mortadella", "café", "yogurt", "pescado"]
    pymes_products = [pymes_arroz, pymes_pollo, pymes_azúcar, pymes_frijoles, pymes_aceite, pymes_picadillo, pymes_mortadella, pymes_café, pymes_yogurt, pymes_pescado]
    canasta_products = [canasta_arroz, canasta_pollo, canasta_azúcar, canasta_frijoles, canasta_aceite, canasta_picadillo, canasta_mortadella, canasta_café, canasta_yogurt, canasta_pescado]

    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(go.Bar(x= products, y= pymes_products, name='Mipymes'), row=1, col=1)
    fig.add_trace(go.Bar(x= products, y= canasta_products, name='Canasta Básica'), row=1, col=2)

    fig.update_xaxes( tickvals=list(range(len(products))),  ticktext=products, tickangle=30 )
    fig.update_layout(title="Gráficas comparativas del costo de los principales productos de la canasta básica contra los productos vendidos por mipymes")
    fig.show()
    
# def qvapay_vs_el_toque():
#   fechas = [fecha['date_from'] for fecha in mf.intervalo_fechas('2025-11-1','2025-11-30', False, False)]
#   usd_qvapay = []
#   for fecha in fechas:
#     offers = []
#     for offer in qvapay:
#       if qvapay[offer]["date"][:10] == fecha and qvapay[offer]["coin"] == "CUP":
#          offers.append(qvapay[offer]["price"])  
#     usd_qvapay.append(offers)
#   medias_qvapay = [ float(mf.mean(m)) for m in usd_qvapay]
#   medias_el_toque = [el_toque[fecha]['USD'] for fecha in fechas]
#   fig = go.Figure(data=[
#     go.Line(name="El Toque", x=fechas, y=medias_el_toque),
#     go.Line(name="QvaPay", x=fechas, y=medias_qvapay)
#   ])
#   fig.update_layout( barmode='group', title= "Gráfica comparativa de los precios media del USD entre El Toque y QvaPay en el transcurso del mes de noviembre de 2025.")
#   fig.show()

# def minorista_vs_mayorista():
#    minoristas = [ [ usd * última_tasa["USD"] for usd in mf.dict_num_values(mipymes[i])] if mipymes[i]["currency"] == "USD" else
#                  [ usd * última_tasa["ECU"] for usd in mf.dict_num_values(mipymes[i])] if  mipymes[i]["currency"] == "EUR"
#                  else mf.dict_num_values(mipymes[i])  for i in  mipymes if mipymes[i]["sales_category"] == "minorista"]
#    mayoristas = [ [ usd * última_tasa["USD"] for usd in mf.dict_num_values(mipymes[i])] if mipymes[i]["currency"] == "USD" else
#                  [ usd * última_tasa["ECU"] for usd in mf.dict_num_values(mipymes[i])] if mipymes[i]["currency"] == "EUR"
#                  else mf.dict_num_values(mipymes[i]) for i in mipymes if mipymes[i]["sales_category"] == "mayorista" ]
   
#    media_minorista = mf.median(mf.aplanar_lista(minoristas))
#    media_mayorista = mf.median(mf.aplanar_lista(mayoristas))

#    fig = go.Figure(data=[
#       go.Bar(x= ["Minorista"], y= [media_minorista], name="Minorista"),
#       go.Bar(x= ["Mayorista"], y= [media_mayorista], name="Mayorista")
#    ])

#    fig.update_layout(title= "Gráfica comparando el precio medio entre los preductos vendidos de forma minorista y de forma mayorista.")
#    fig.show()

def bar_compare_coin():
   usd = mf.mean(list(map(lambda x: x*última_tasa["USD"], mf.aplanar_lista([mf.dict_num_values(mipymes[p]["products"]) for p in mipymes_usd]))))
   eur = mf.mean(list(map(lambda x: x*última_tasa["ECU"], mf.aplanar_lista([mf.dict_num_values(mipymes[p]["products"]) for p in mipymes_eur]))))
   cup = mf.mean(mf.aplanar_lista([mf.dict_num_values(mipymes[p]["products"]) for p in mipymes_cup]))
   coins = ["USD", "EUR", "CUP"]

   fig = go.Figure(
      data= go.Bar(x=coins, y=[usd, eur, cup], marker=dict(color= ["red", "yellow", "green"]))
   )
   fig.update_layout(title="Gráfica demostrativa de que el precio del CUP está influyendo en el precio de los productos en mipymes cubanas.")
   fig.show()





