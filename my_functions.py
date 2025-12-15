from typing import List
import json
from json import JSONDecodeError
from datetime import datetime, timedelta
from urllib.parse import urlencode
import subprocess
import sys
import re
from functools import reduce

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

def multi_replace(text:str, dict_replace: dict[str,str] = {'' : ''}, space: bool = False)  -> str:
  list_text = text.split()
  palabras = [ p.strip() for p in list_text]
  if space:
    text = ' '.join(palabras)
    for i in dict_replace.keys():
      text = text.replace(i, dict_replace[i])
  else:
    for i in dict_replace.keys():
      text = text.replace(i, dict_replace[i])
  return text

def write_file(origen: str, destino: str, replaces: dict[str,str] =  {'' : ''}, space = False):
   with open(origen, "r") as file:
    text = file.read()
    with open(destino, "w") as wr:
      wr.write(multi_replace(text, replaces, space))

def py_compile(destino: str):
  return subprocess.run(['cythonize',  '--inplace', destino],  capture_output=True, text=True).stdout

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
   return [ data[i][second_key] for i in data if str(data[i][key]).upper().replace(' ','') == value.upper().replace(' ','')]

def first_count(lista:list[str], elemento:str):
  contador = 0
  for i in lista:
    if elemento.upper().replace(' ','') in i.upper().replace(' ',''):
       contador += 1
  return contador

def search_keys(dict: dict[str,float], key=str):
    new_dict = {}
    keys = [ k for k  in dict]
    for k in keys:
        if key.upper().replace(' ','') in k.upper().replace(' ',''):
            new_dict[k] = dict[k]
        else:
            continue
    return new_dict

def dict_num_values(dicc: dict) -> list:
   values =  []
   if type(dicc) == dict:
      for i in dicc.values():
          if type(i) == int or type(i) == float:
              values.append(i)
          else:
              values.extend(dict_num_values(i))
   return values

def dict_keys(diccionary : dict):
   lista = []
   if type(diccionary) == dict:
      for k in diccionary.keys():
          if type(k) == str or type(k) == str:
              lista.append(k)
          else:
              lista.extend(dict_keys(k))
   return lista

def aplanar_lista(lista: list = []) -> list:
    lista_aplanada = []
    n = len(lista) 
    if n == 0: 
        return lista_aplanada
    for i in lista:
        if not isinstance(i,list):
            lista_aplanada.append(i)
        else:
            lista_aplanada.extend(aplanar_lista(i))
    return lista_aplanada

def parser_qvapay(id: str, date: str, text: str, file: str) -> str:
    '''
    Esta función permite guardar en un archivo json una oferta obtenida de un mensaje de qvapay. Se recibe como parámetros de entrada el id ,
    la fecha y hora y el texto del mensaje obtenido de telegram.
    '''
    ratio = float(re.search(r"Ratio:\s*\$([0-9]+\.[0-9]+)", text).group(1))
    text = text.split()
    operation = you_type(text[1][1:])
    coin = you_type(text[6][1:])
    offers = read_json(file)
    offers[id] = {
        "date": date,
        "operation": operation,
        "coin": coin,
        "price": ratio
    }
    save_json(offers, file)
    return f"Se ha guardado la oferta {id}."

def sum_rows(matriz: list) -> list[int|float]:
    try:
        n = len(matriz)
        if n == 1:
           return matriz
        if all( str(i).isnumeric() for i in matriz):
           return matriz
        m = len(matriz[0])
        for r in matriz:
           if len(r) != m:
              return IndexError
        aux = []
        row = []
        for i in range(m):
            for j in range(n):
              aux.append(matriz[j][i])
        for s in range(0,m*n,n):
          suma = sum([aux[m] for m in range(s,s+n)])
          row.append(suma)
        return row
    except IndexError as e:
       return e
    
def rest_row(matriz: list) -> list[int|float]:
    try:
        n = len(matriz)
        if n == 1:
           return matriz
        if all( str(i).isnumeric() for i in matriz):
           return matriz
        m = len(matriz[0])
        for r in matriz:
           if len(r) != m:
              return IndexError
        aux = []
        row = []
        for i in range(m):
            for j in range(n):
              aux.append(matriz[j][i])
        for s in range(0,m*n,n):
          resta = reduce(lambda x, y: x-y,[aux[m] for m in range(s,s+n)])
          row.append(resta)
        return row
    except IndexError as e:
       return e
          
def list_to_dict(keys: list[str], values: list) -> dict:
  n,m = len(keys), len(values)
  if n != m or n == m == 0:
    if n > m:
      values.extend([None for _ in range(n-m)])
    else:
     return False
  dict = {}
  for i in range(n):
    dict[keys[i]] = values[i]
  return dict

def insert_in_list(iter: list, element, index: int = -1):
    left = iter[:index]
    right = iter[index:]
    if index == -1:
       return iter + [element]
    if index == 0:
        return [element] + iter
    return  left + [element] + right
  
def dict_for_index(dict: dict, index: int):
    '''
    Con esta función podrá accder aun valor de un diccionario por el indice de su respectiva clave.
    '''
    keys = [k for k in dict]
    key = keys[index]
    return dict[key]

def mean(lista: list = []) -> float:
  n = len(lista)
  if n == 0:
    return 0
  return float(sum(lista) / n)

def median(lista: list) -> float:
  n = len(lista)
  lista = sorted(lista)
  if n == 0:
    return 0
  if n % 2 != 0:
    return float(lista[(n-1)//2])
  return  float((lista[(n-1)//2] + lista[n//2]) / 2)

def del_dict_in_sec(dict: dict, key:str="", first:int=0):
    '''
    Con esta función podrá eliminar claves pares clave valor de diccionario con claves numéricas perder orden ni secuencia.
    Los valores de entrada para esta función son el diccionario , la clave que se quiere eliminar y opcionalmente el indice en que comenzará la nueva secuencia.
    '''
    new_values =  [dict[k] for k in dict if k != key]
    n = len(new_values)
    new_dict = {}
    if first == n:
        new_dict.update({str(first): new_values[0]})
    for i in range(first, n):
        new_dict.update({str(i): new_values[i]})
    return new_dict

def max_objects(object: list[int|float], max_sum : int) -> int:
    matriz = [-sys.maxsize] * (max_sum+1)
    matriz[0] = 0
    for i in object:
        for j in range(max_sum, i - 1, -1):
            matriz[j] = max(matriz[j], matriz[j - i] + 1)
    return int(max(matriz))

def redondear(n: float) -> int:
   left = int(n)
   right = left+1
   if n <= left+0.5:
      return left
   else:
      return right
   