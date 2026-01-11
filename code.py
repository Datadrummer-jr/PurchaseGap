import my_functions as mf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

el_toque = mf.read_json('data/el_toque.json')
salarios = mf.read_json("data/escalas_salariales.json")
cities = mf.read_json("data/cities.json")
muni = mf.read_json("data/municipality_country.json")
abreviaturas = mf.read_json('data/abreviaturas.json')
city = ["HAB", "PRI", "ART", "MAY", "MTZ", "CFG", "VCL", "SSP", "CAV", "CAM", "LTU", "GRM", "HOL", "SCU", "GTM", "IJV"]
data = mf.read_json("data/pymes.json")
mipymes = mf.read_json("data/prices_pymes.json")
población_por_provincia =mf.read_json("data/población_cuba (2024).json")
canasta_básica = mf.read_json("data/canasta_básica.json")
qvapay = mf.read_json("data/qvapay.json")
amazon = mf.read_json("data/amazon.json")
latam_salary = mf.read_json("data/latam_salary.json")
ventas_2024 = mf.read_json("data/ventas_minoristas (2024).json")
mapcuba = mf.read_json(r"data\\geo_json\\geojson_by_region_division\\by_provinces\\cuba.geojson")

last_rate = mf.dict_for_index(el_toque,-1)

mipymes_cup = {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "CUP"}
mipymes_usd =  {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "USD"}
mipymes_eur = {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "EUR"}

def salary(file = salarios):
   for i in range(0,32):
     print(f"{i} | 44 horas: {file['44_horas'][i]} | 40 horas : {file['40_horas'][i]}")

def graph_coin():
  tasas = [el_toque[i['date_from']] for i in mf.intervalo_fechas("2025-01-01", "2025-12-31",False,False) if el_toque[i['date_from']] is not None]
  days = [day['date_from'] for day in mf.intervalo_fechas("2025-01-01", "2025-12-31",False,False) ]
 
  usd = [i["USD"] for i in tasas]
  euro = [i["ECU"] for i in tasas]
  mlc = [i["MLC"] for i in tasas]

  fig = go.Figure(data=[
  go.Scatter(x=days, y=usd, mode="lines", name= 'USD'),
  go.Scatter(x=days, y=euro, mode="lines", name= 'EURO'),
  go.Scatter(x=days, y=mlc, mode="lines", name= 'MLC')
  ]
  )
  
  fig.update_layout(width=1100, height=600, title='Comparación del comportamiento del USD, el EURO y el MLC a lo largo de todo 2025.')
  fig.write_image("static_charts/graph_coin.png")  
  fig.show()
      
def compra_por_escala(escala: int):
   máximos = [mf.max_objects([mf.redondear(i*last_rate["ECU"])for i in mf.dict_num_values(mipymes[i]['products'])], escala) 
              if  mipymes[i]["currency"] == "EUR" 
              else
              mf.max_objects([mf.redondear(i*last_rate["USD"])for i in mf.dict_num_values(mipymes[i]['products'])], escala) 
              if mipymes[i]["currency"] == "USD"
              else mf.max_objects([mf.redondear(i) for i in mf.dict_num_values(mipymes[i]['products'])], escala) 
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
  fig.update_layout(width=1200, height=600, title='Mediana de la cantidad máxima de productos que se pueden adquirir en un establecimiento de comercio según escala salarial.')
  fig.write_image("static_charts/max_bar.png")  
  fig.show()

def price_media(product: str):
  canasta =  mf.aplanar_lista(mf.dict_num_values(mf.search_keys(canasta_básica, product)))
  usd = list(map(lambda x: x* last_rate["USD"],  mf.aplanar_lista([mf.dict_num_values(mf.search_keys(mipymes_usd[a]["products"], product)) for a in mipymes_usd ])))
  eur = list(map(lambda x: x*last_rate['ECU'], mf.aplanar_lista([mf.dict_num_values(mf.search_keys(mipymes_eur[a]["products"], product)) for a in mipymes_eur ])))
  cup= mf.aplanar_lista([mf.dict_num_values(mf.search_keys(mipymes_cup[a]["products"], product)) for a in mipymes_cup])
  return mf.median(cup+usd+eur) , mf.median(canasta)

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

pymes_huevo, canasta_huevo = price_media("CARTON DE HUEVO")

def canasta_vs_pymes():
    products = ["arroz", "pollo" , "azúcar", "frijoles", "aceite", "picadillo", "mortadella", "café", "yogurt", "pescado", "huevo" ]
    pymes_products = [pymes_arroz, pymes_pollo, pymes_azúcar, pymes_frijoles, pymes_aceite, pymes_picadillo, pymes_mortadella, pymes_café, pymes_yogurt, pymes_pescado, pymes_huevo]
    canasta_products = [canasta_arroz, canasta_pollo, canasta_azúcar, canasta_frijoles, canasta_aceite, canasta_picadillo, canasta_mortadella, canasta_café, canasta_yogurt, canasta_pescado, canasta_huevo]

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Mipymes", "Canasta Básica"])

    fig.add_trace(go.Bar(x= products, y= pymes_products, name='Mipymes'), row=1, col=1)
    fig.add_trace(go.Bar(x= products, y= canasta_products, name='Canasta Básica'), row=1, col=2)

    fig.update_xaxes( tickvals=list(range(len(products))),  ticktext=products, tickangle=30 )
    fig.update_layout(width=1100, height=600, title="Gráficas comparativas del costo medio de productos de la canasta básica contra los vendidos por mipymes.")
    fig.write_image("static_charts/canasta_vs_pymes.png")  
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

def max_buy_latam():
   names_products = mf.aplanar_lista([mf.dict_keys(amazon[a]) for a in amazon])
   prices_products = mf.aplanar_lista([mf.dict_num_values(amazon[a]) for a in amazon])
   uni_products = mf.list_to_dict(names_products, prices_products)
   salaries = [mf.redondear(latam_salary[s]) for s in latam_salary]
   max_buy = [ mf.max_objects([mf.redondear(i) for i in mf.dict_num_values(uni_products)], s) for s in salaries]

   fig = go.Figure(data= go.Bar(
      x= [c for c in latam_salary],
      y = max_buy,
      marker=dict(color= ["green"]*6 + ["red"] + ["green"]*13)
    ))
   fig.update_layout(width=1100, height=600, title="¿ Cuáles serán los paises de latinoamérica que más productos pueden comprar en Amazon con un salario mínimo ? ")
   fig.write_image("static_charts/max_buy_latam.png") 
   fig.show()

def ventas_minoristas():
   total = ventas_2024["2024.0"]["Total"]
   products = ["Comestibles", "Bebidas alcohólicas", "Cervezas", "Tabaco y cigarros", "Otros"]
   count = [ ventas_2024["2024.0"][i] for i in products[:-1]]
   count.append(total-sum(count))
   fig = go.Figure(
      data=[
         go.Pie(
            labels = products,
            values = count
         )
      ]
   )
   fig.write_image("static_charts/ventas_minoristas.png") 
   fig.show()

def mayor_alcance():
   alimentos =  [
    "pollo", "cerdo", "res", "carne", "jamon", "jamón", "pescado", "atun", 
    "atún", "sardina", "salchicha", "hamburguesa", "bistec", "costilla", 
    "lomo", "huevo", "arroz", "frijol", "lenteja", "garbanzo", "pasta", 
    "espagueti", "spaghetti", "pizza", "pan", "galleta", "cereal", "harina", 
    "leche", "queso", "yogurt", "helado", "mantequilla", "aceite", "vinagre", 
    "salsa", "mayonesa", "ketchup", "mostaza", "tomate", "fruta", "vegetal", 
    "ensalada", "refresco", "jugo", "agua mineral", "agua natural", "agua gourmet", 
    "café", "cafe ", "malta", "chocolate", "cacao", "tarta", "dulce", 
    "mermelada", "croqueta", "empanada", "tostones", "vianda"
   ]

   bebidas_alcoholicas = [
    "ron", "whisky", "vodka", "tequila", "aguardiente", "sangría", "licor", "vino", "espumoso", "champán", "anis",
    "cerveza", "cubay", "havana club", "ballantine", "chivas", "absolut", "jagermeister", "profundo", "vigia", "black tears"
   ]

   pymes_alimentos = [mf.max_objects(mf.dict_num_values(mf.search_keys(mipymes_cup[k]["products"], subk)), salarios["44_horas"][-1]) for subk in alimentos for k in mipymes_cup if mf.dict_num_values(mf.search_keys(mipymes_cup[k]["products"], subk))] + \
                 [mf.max_objects([price * last_rate["USD"] for price in mf.dict_num_values(mf.search_keys(mipymes_usd[k]["products"], subk))], salarios["44_horas"][-1]) for subk in alimentos for k in mipymes_usd ] +\
                 [mf.max_objects([price * last_rate["ECU"] for price in mf.dict_num_values(mf.search_keys(mipymes_eur[k]["products"], subk))], salarios["44_horas"][-1]) for subk in alimentos for k in mipymes_eur ]

   pymes_bebidas = [mf.max_objects(mf.dict_num_values(mf.search_keys(mipymes_cup[k]["products"], subk)), salarios["44_horas"][1]) for subk in bebidas_alcoholicas for k in mipymes_cup if mf.dict_num_values(mf.search_keys(mipymes_cup[k]["products"], subk))] + \
                 [mf.max_objects([price * last_rate["USD"] for price in mf.dict_num_values(mf.search_keys(mipymes_usd[k]["products"], subk))], salarios["44_horas"][-1]) for subk in bebidas_alcoholicas for k in mipymes_usd ] +\
                 [mf.max_objects([price * last_rate["ECU"] for price in mf.dict_num_values(mf.search_keys(mipymes_eur[k]["products"], subk))], salarios["44_horas"][1]) for subk in bebidas_alcoholicas for k in mipymes_eur ]
   
   print(max(mf.del_value(pymes_alimentos, 0)))
   print(max(mf.del_value(pymes_bebidas, 0)))

   fig = go.Figure(
      data= 
         go.Bar(
            x=["Alimentos", "Bebidas Alcoholicas"],
            y = [mf.median(mf.del_value(pymes_alimentos, 0)), mf.median(mf.del_value(pymes_bebidas, 0))]
         )
   )
   fig.show()

def ipc():
   fao_2010 = mf.read_json(r"data\\FAO_2010.json")
   ipc_global = mf.read_json(r"data\\IPC-FAO.json")
   ipc_cuba = mf.read_json(r"data\\IPC-Cuba.json")

   months = [month for month in ipc_global][:48]
   ipc_fao_2021_2024 = [(ipc_global[month] / fao_2010[month.split()[0]]) *100 for month in ipc_global]
   ipc_cuba_2021_2024= mf.dict_num_values(ipc_cuba)

   fig = go.Figure(data=[
      go.Scatter(x=months, y=ipc_cuba_2021_2024, name="Cuba", mode="lines+markers"),
      go.Scatter(x=months, y=ipc_fao_2021_2024, name="Mundial", mode="lines+markers")
   ])
   fig.update_xaxes(
   tickvals=[0,12,24,36],  
    ticktext= [2021,2022,2023,2024],  
    tickangle=0
   )
   fig.update_layout(width=1100, height=600, title="Comparativa del indice de precios al consumidor de Cuba con el resto del mundo con respecto a 2010.")
   fig.write_image("static_charts/ipc.png")
   fig.show()

def coin_pymes():
   cup = mf.aplanar_lista([ mf.dict_num_values(mipymes_cup[c]["products"]) for c in mipymes_cup])
   usd = [ d * last_rate["USD"] for d in mf.aplanar_lista([ mf.dict_num_values(mipymes_usd[c]["products"]) for c in mipymes_usd])]
   euro = [d * last_rate["ECU"] for d in mf.aplanar_lista([ mf.dict_num_values(mipymes_eur[c]["products"]) for c in mipymes_eur])]
   
   fig = go.Figure(data=
      go.Bar(x=["CUP", "Monedas Extrajeras"], y=[mf.median(cup), mf.median(usd+euro)])
   )
   fig.update_layout(width=1100, height=600, title="Comparativa del precio medio de entre las mipymes en moneda nacional y en monedas extrajeras en Cuba.")
   fig.write_image("static_charts/coin_pymes.png")
   fig.show()

count_pymes = [mf.first_count(mf.list_for_value(data, key='city', value= i.upper().replace(' ',''), second_key= "subject"), "MIPYME") for i in cities ]
población  = [ población_por_provincia[abreviaturas[i]]["total"] for i in city]
for_hab = [ int(población[i] // count_pymes[i]) for i in range(len(población))]

def personas_por_mipyme():
   df = {
      "Provincia": cities,
      "Habitantes": población,
      "Mipymes": count_pymes,
      "Mipymes por habitantes": for_hab
   }
   fig = px.choropleth_mapbox(
        data_frame= df,
        geojson=mapcuba,
        locations= "Provincia",
        featureidkey="properties.province",
        color= "Mipymes por habitantes" ,
        color_continuous_scale="Reds",
        range_color=[min(df["Mipymes por habitantes"]), max(df["Mipymes por habitantes"])],  # Rango de valores
        mapbox_style="carto-positron",
        zoom=6,
        center={"lat": 21.5, "lon": -80},
        opacity=0.7,
        hover_name= "Provincia",
        hover_data={
            "Habitantes": ':,',
            "Mipymes": ':,',
            "Mipymes por habitantes": ':,',

        },
        title="Cantodad de mipymes por habitantes en Cuba"
    )

   fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        width=1150,
        height=700
    )
   fig.write_html("static_charts/personas_por_mipyme.html")
   fig.show()





   
