import requests
import pandas as pd
from datetime import datetime
from obtener_datos_frontera import obtener_datos_frontera

# Leer el archivo Excel con los valores de sic_code
sic_codes_df = pd.read_excel('/Users/luiscarlosparraraffan/Desktop/NEU API/FronterasNeu.xlsx', header=None)
date = '2025-03-02'




# Crear un dataframe vacío para almacenar los resultados
Fronteras = pd.DataFrame()

# Recorrer todos los valores de sic_code y obtener los datos de frontera
for sic_code in sic_codes_df.iloc[:, 0]:
    Frontera = obtener_datos_frontera(sic_code, date)
    if Frontera is not None:
        Fronteras = pd.concat([Fronteras, Frontera], ignore_index=True)

# Guardar el DataFrame resultante en un archivo Excel
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"Fronteras_{date}_{current_time}.xlsx"
Fronteras.to_excel(file_name, index=False)
print(f"Archivo guardado como: {file_name}")