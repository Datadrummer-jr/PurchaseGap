
import xlrd
import openpyxl
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import my_functions as mf
import datetime

ruta_población = r"..\\sources\\20251030-aec2024-excel-capitulos-publicados\\03 Poblacion_AEC2024.xls"
rute_ipc = r"D:\DATA SCIENCE\Programación\Data-Pyme\sources\IPC\food_price_indices_data_dec.xlsx"
ruta_ventas_minoristas = r"..\\sources\\20251030-aec2024-excel-capitulos-publicados\\14 Comercio Interno_AEC2024.xlsx"

def población():
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

def ipc(base: bool= False):
    excel = openpyxl.load_workbook(rute_ipc)
    hoja = excel.worksheets[0]
    Years = [ (cell.value.strftime("%B %Y") if isinstance(cell.value, datetime.datetime) else cell.value) for cell in hoja["A"] ]
    values = [cell.value for cell in hoja["B"]]
    
    if base:
        Years = Years[244:256]
        values = values[244:256]
        
    else:
        Years = Years[376:424]
        values = values[376:424]
    
    FAO_IPC = mf.read_json(r"..\\data\\IPC-FAO.json")

    for i in range(len(Years)):
        FAO_IPC[Years[i]] = float(values[i])
    
    mf.save_json(FAO_IPC, r"..\\data\\IPC-FAO.json")

if __name__ == "__main__":
    ipc()



