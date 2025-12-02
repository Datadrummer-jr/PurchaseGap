
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

mf.save_json(población_por_city, r"..\\data\\población_cuba (2024).json")