
import xlrd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import my_functions as mf

ruta_población = r"..\\sources\\20251030-aec2024-excel-capitulos-publicados\\03 Poblacion_AEC2024.xls"
población = xlrd.open_workbook(ruta_población)
sheet = población.sheet_by_index(2)

población_por_city = {}

for i in range(7, 40, 4):
    población_por_city[sheet.cell_value(i,0).strip()] = {
      "total": sheet.cell_value(i,6),
      "hombres": sheet.cell_value(i+1,6),
      "mujeres": sheet.cell_value(i+2,6),
      "Razón por sexo": sheet.cell_value(i+3,6),
   }
    
for j in range(53, 84, 4):
    población_por_city[sheet.cell_value(j,0).strip()] = {
      "total": sheet.cell_value(j,6),
      "hombres": sheet.cell_value(j+1,6),
      "mujeres": sheet.cell_value(j+2,6),
      "Razón por sexo": sheet.cell_value(j+3,6),
   }

# mf.save_json(población_por_city, r"..\\data\\población_cuba (2024).json")

ruta_ventas_minoristas = r"..\\sources\\20251030-aec2024-excel-capitulos-publicados\\14 Comercio Interno_AEC2024.xlsx"
ventas_minoristas = xlrd.open_workbook(ruta_ventas_minoristas)
sheet =  ventas_minoristas.sheet_by_name("14-6")

ventas = {}

for i in range(13,30):
    ventas[str(mf.you_type(sheet.cell_value(i,0))).strip()] = {
        "Total": round(sheet.cell_value(i,1), 2),
        "Comestibles": round(sheet.cell_value(i,2), 2),
        "Bebidas alcohólicas": round(sheet.cell_value(i,3), 2),
        "Cervezas": round(sheet.cell_value(i,4), 2),
        "Tabaco y cigarros": round(sheet.cell_value(i,5), 2)
    }

mf.save_json(ventas, r"..\\data\\ventas_minoristas (2024).json")