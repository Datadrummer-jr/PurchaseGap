import my_functions as mf
import plotly.graph_objects as go
import plotly.express as px

el_toque = mf.read_json('data/el_toque.json')
salaries = mf.read_json("data/salary_for_activity.json")
cities = mf.read_json("data/cities.json")
muni = mf.read_json("data/municipality_country.json")
abreviaturas = mf.read_json('data/abreviaturas.json')
city = ["HAB", "PRI", "ART", "MAY", "MTZ", "CFG", "VCL", "SSP", "CAV", "CAM", "LTU", "GRM", "HOL", "SCU", "GTM", "IJV"]
data = mf.read_json("data/pymes.json")
mipymes = mf.read_json("data/prices_pymes.json")
población_por_provincia =mf.read_json("data/población_cuba (2024).json")
canasta_básica = mf.read_json("data/canasta_básica.json")
amazon = mf.read_json("data/amazon.json")
latam_salary = mf.read_json("data/latam_salary.json")
mapcuba = mf.read_json(r"data\\geo_json\\geojson_by_region_division\\by_provinces\\cuba.geojson")

last_rate = mf.dict_for_index(el_toque,-1)

mipymes_cup = {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "CUP"}
mipymes_usd =  {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "USD"}
mipymes_eur = {k: mipymes[k] for k in mipymes if mipymes[k]["sales_category"] == "minorista" and mipymes[k]["currency"] == "EUR"}

def graph_coin():
  rate = [el_toque[i['date_from']] for i in mf.days_range("2025-01-01", "2025-12-31",False,False) if el_toque[i['date_from']] is not None]
  days = [day['date_from'] for day in mf.days_range("2025-01-01", "2025-12-31",False,False) ]
 
  usd = [i["USD"] for i in rate]
  euro = [i["ECU"] for i in rate]
  mlc = [i["MLC"] for i in rate]

  fig = go.Figure(data=[
  go.Scatter(x=days, y=usd, mode="lines", name= 'USD'),
  go.Scatter(x=days, y=euro, mode="lines", name= 'EURO'),
  go.Scatter(x=days, y=mlc, mode="lines", name= 'MLC')
  ]
  )
  
  fig.update_layout(width=1100, height=600, title='Comparación del comportamiento del USD, el EURO y el MLC a lo largo de todo 2025.')
  fig.write_image("static_charts/graph_coin.png")  
  fig.show()
      
def buy_for_activity(salary: int):
   max = [mf.max_objects([i for i in mf.dict_num_values(mipymes[i]['products'])], salary) 
              for i in mipymes]
   return  int(mf.median(max))

def max_bar():
  max_products = [buy_for_activity(s) for s in mf.dict_num_values(salaries)]
  count_salaries = list(range(len(max_products)))
  fig = go.Figure(data=[
     go.Bar(x= max_products, y= count_salaries, orientation="h", marker=dict(color="yellow"))
  ])
  fig.update_yaxes(
    tickvals= count_salaries,  
    ticktext= mf.dict_keys(salaries),  
    tickangle=0
  )
  fig.update_layout(width=1200, height=600, title='Mediana de la cantidad máxima de productos que se pueden adquirir en un establecimiento de comercio según escala salarial.')
  fig.write_image("static_charts/max_bar.png")  
  fig.show()

def price_media(product: str):
  canasta =  mf.plain_list(mf.dict_num_values(mf.search_keys(canasta_básica, product)))
  cup= mf.plain_list([mf.dict_num_values(mf.search_keys(mipymes_cup[a]["products"], product)) for a in mipymes_cup])
  return mf.median(cup) , mf.median(canasta)

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
    division = [pymes_products[i] // canasta_products[i] for i in range(len(products))]
    fig = go.Figure(data=
      go.Bar(x=products, y= division)
    )
    
    fig.update_layout(width=1100, height=600, title="Gráficas que muestra cuantas veces es el precio de los productos de la canasta básica en las mipymes.")
    fig.write_image("static_charts/canasta_vs_pymes.png")  
    fig.show()

def max_buy_latam():
   names_products = mf.plain_list([mf.dict_keys(amazon[a]) for a in amazon])
   prices_products = mf.plain_list([mf.dict_num_values(amazon[a]) for a in amazon])
   uni_products = mf.list_to_dict(names_products, prices_products)
   salaries = [mf.float_to_best_int(latam_salary[s]) for s in latam_salary]
   max_buy = [ mf.max_objects([mf.float_to_best_int(i) for i in mf.dict_num_values(uni_products)], s) for s in salaries]

   fig = go.Figure(data= go.Bar(
      x= [c for c in latam_salary],
      y = max_buy,
      marker=dict(color= ["green"]*6 + ["red"] + ["green"]*13)
    ))
   fig.update_layout(width=1100, height=600, title="¿ Cuáles serán los paises de latinoamérica que más productos pueden comprar con un salario mínimo ? ")
   fig.write_image("static_charts/max_buy_latam.png") 
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

count_pymes = [mf.first_count(mf.list_for_value(data, key='city', value= i.upper().replace(' ',''), second_key= "subject"), "MIPYME") for i in cities ]
población  = [ población_por_provincia[abreviaturas[i]]["total"] for i in city]
for_hab = [ int(población[i] // count_pymes[i]) for i in range(len(población))]

def pymes_for_person():
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





   
