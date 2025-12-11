import pdfplumber
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import my_functions as mf

cities = mf.read_json('../data/cities.json')
abreviaturas = mf.read_json('../data/abreviaturas.json')
municipios_por_provincia = mf.read_json('../data/municipality_country.json')
mipymes_actuales = mf.read_json('../data/pymes.json')
rute_pymes = '../sources/Listado de Nuevos Actores Económicos aprobados hasta 09.05.24 .pdf'

def formate_pyme(lista:list) ->bool:
  if str(lista[0]).isdigit():
    return True
  return False

def save_pyme(index: int):
  with pdfplumber.open(rute_pymes) as pdf:
    mipymes = pdf.pages[index].extract_tables()
    mipymes = [ mf.del_salto(i) for i in mf.detectar_lista(lista=mipymes,key=formate_pyme) ]
    cantidad = len(mipymes)

    indices = [ i[0] for i in mipymes]
    name = [ n[1] for n in mipymes]
    city = [ c[2] for c in mipymes]
    type = [ t[-2] for t in mipymes]
    activity = [ a[-1] for a in mipymes]

    for i in range(cantidad):
      if len(city[i]) > 3:
       mipymes_actuales[indices[i]] = {'name': name[i], 'city': str(city[i]).upper(), 'subject': str(type[i]).upper(), 'activity':activity[i] }
      else:
        mipymes_actuales[indices[i]] = {'name': name[i], 'city': abreviaturas[city[i]].upper(), 'subject': str(type[i]).upper(), 'activity':activity[i] }
    
    mf.save_json(mipymes_actuales,'../data/pymes.json')
    
if __name__ == '__main__':
  # Recomiendo que se scrapee por tramos en vez de todo de una vez:

  # for i in range(len(pdfplumber.open(rute_pymes).pages)):
  #   save_pyme(i)
  
  # Opción recomendada:

  # for i in range(100,200):
  #   save_pyme(i)
  pass
  