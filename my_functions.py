from typing import List, Tuple
import numpy as np
import plotly.graph_objects as go
import json
from json import JSONDecodeError
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime, timedelta
from urllib.parse import urlencode
import subprocess
import re

def you_type(cadena):
  if type(cadena) == int:
     return int(cadena)
  if type(cadena) == float:
     return float(cadena)
  if type(cadena) == str:
   if cadena.isdigit():
     return int(cadena)
   caracteres = [l for l in cadena]
   if cadena == "":
    return None
   n = len(cadena)
   if caracteres[0] == "." and cadena[1:n].isdigit():
    return float(cadena)
   if cadena[0] == "-":
    return float(cadena.strip())
   else:
    for i in cadena:
      if "." in caracteres and i.isdigit():
        return float(cadena)
      else:
        return str(cadena)
  return False

def max_valor(matrix: List[List[int]]) -> List[List[int]]:
  matrix = np.array(matrix)
  traspuesta = matrix.T
  sumas = []
  for i in range(len(traspuesta)):
    sumas.append(float(sum(list(filter(lambda x: x!= None , traspuesta[i])))))
  maximo = max(sumas)
  return sumas.index(maximo)

def min_valor(matrix: List[List[int]]) -> List[List[int]]:
  matrix = np.array(matrix)
  traspuesta = matrix.T
  sumas = []
  for i in range(len(traspuesta)):
    sumas.append(float(sum(list(filter(lambda x: x!= None , traspuesta[i])))))
  maximo = min(sumas)
  return sumas.index(maximo)

def my_protly(x: List[int], y: List[int], line: str, title: str, eje_x : str, eje_y: str, name_legend: str, colors : str = "royalblue") -> None:
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name= line, line=dict(color=colors)))
  fig.update_layout(
    title=title,
    xaxis_title=eje_x,
    yaxis_title=eje_y,
    legend_title=name_legend
  )
  return fig

def doble_y_protly(x: List[int], y: List[List[int]], line: List[str], colors : List[str], title: str, eje_x : str, eje_y: str, name_legend: str) -> None:
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=x, y=y[0], mode='lines+markers', name= line[0], line=dict(color=colors[0])))
  fig.add_trace(go.Scatter(x=x, y=y[1], mode='lines+markers', name= line[1], line=dict(color=colors[1])))
  fig.update_layout(
    title=title,
    xaxis_title=eje_x,
    yaxis_title=eje_y,
    legend_title=name_legend
    )
  return fig

def balancear_matrix(matrix: List[List[any]],valor_para_balancear = 0) -> List[List[any]]:
  copy_list = matrix.copy()
  len_maximo = max([ len(v) for v in copy_list])
  for g in copy_list:
   if len(g) < len_maximo:
      diferencia = len_maximo - len(g)
      for _ in range(diferencia):
         g.append(valor_para_balancear)
  return copy_list

def range_in_lists(lista1: List[int], lista2: List[int]) -> List[List[int]]:
  total_lists = []
  n = len(lista1)
  m = len(lista2)
  if n != m:
    return False
  def rango(indice: int):
    numbers = []
    for y in range(lista1[indice], lista2[indice] + 1):
      numbers.append(y)
    return numbers
  for i in range(n):
    total_lists.append(rango(i))
  return total_lists

def element_in_matrix(elemento: any, matrix: List[List[any]]) -> List[Tuple[int,int]]:
  n = len(matrix)
  m = len(matrix[0])
  elements = []
  for i in range(n):
    for j in range(m):
      if matrix[i][j] == elemento:
        elements.append((i,j))
      else:
        continue
  return elements
      
def save_json(datos,file: str) -> None:
  with open(file,"w", encoding="utf-8") as sj:
    json.dump(datos, sj, indent=4, ensure_ascii=False)

def read_json(file: str):
  try:
    with open(file,encoding="utf-8") as rj:
      datos = json.load(rj)
    return datos
  except JSONDecodeError as e:
    return f'Hubo un error de decodificación del json: {e}'

def coeficiente(ind: List[List[int]], dep: List[int], grade : int=1) -> float:
  model = LinearRegression()
  poly = PolynomialFeatures(degree=grade)
  px = poly.fit_transform(np.array(ind).T)
  model.fit(px,np.array(dep))
  coef = model.score(px,dep)
  return coef

def intervalo_fechas(fecha_inicio: str, fecha_fin: str, url: bool = True, time: bool = True) -> List[str]:
    if time:
     date_from = datetime.strptime(f"{fecha_inicio} 00:00:01", "%Y-%m-%d %H:%M:%S")
    else:
     date_from = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    
    if time:
     date_to = datetime.strptime(f"{fecha_fin} 23:59:01", "%Y-%m-%d %H:%M:%S")
    else:
     date_to = datetime.strptime(fecha_fin, "%Y-%m-%d")    

    resultado = []
    current = date_from.date()
    end = date_to.date()

    while current <= end:
        if url and time:
          resultado.append(urlencode({
            "date_from": f"{current} 00:00:01",
            "date_to": f"{current} 23:59:01"
        }))
        
        elif time and not url:
          resultado.append({
            "date_from": f"{current} 00:00:01",
            "date_to": f"{current} 23:59:01"
        })
        elif not time and url:
          resultado.append(urlencode({
            "date_from": f"{current}",
            "date_to": f"{current}"
        }))
        
        else:
          resultado.append({
            "date_from": f"{current}",
            "date_to": f"{current}"
        })
        current += timedelta(days=1)
    return resultado


def one_spce(t:str,f: str,s: str) -> False:
  lista = t.split()
  lista = del_value(lista)
  for i in range(0, len(lista)-1):
    if lista[i] == f and lista[i+1] == s:
      return True
  return False

def write_file(origen: str, destino: str,replace_of: str="" ,replace_for: str=""):
  with open(origen, "r") as file:
    text = file.read()
  with open(destino, "w") as wr:
    wr.write(text.replace(replace_of,replace_for))
  return subprocess.run(['python', 'setup.py', 'build_ext', '--inplace'],  capture_output=True, text=True).stdout

def del_value(lista: list , value = '') -> List:
  return [ i for i in lista if i != value ]
  
def del_space(lista: list) -> list:
  return [i.strip() for i in lista]

def del_salto(lista: list) -> list:
  return [i.replace('\n', ' ') for i in lista  if i is not None if type(i) == str]

def pto_final(lista: list) -> list:
  return [i[:-1] for i in lista if i[-1] == '.']

def detectar_lista(lista: list, key: function) -> list:
  salida = []
  for i in lista:
    if type(i) == list:
      if len(i) > 0 and key(i):
        salida.append(i)
      else:
        salida.extend(detectar_lista(i, key))
  return salida

def list_for_value(data: dict[dict], key:str,value: str =None, second_key=None):
  if type(data) == dict:
   return [ data[i][key] for i in data if str(data[i][key]).replace(' ','') == value]





