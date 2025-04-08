import requests
import pandas as pd
from datetime import datetime

def obtener_datos_frontera(sic_code, date):
    # Convert the input date to the required format
    from_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00Z")
    to_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%dT23:00:00Z")
    
    # URL de la API
    url = "https://api.neu.com.co/ddv/consumption"

    # Cabeceras de la petición, incluyendo el token de autenticación
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjYzMTQiLCJlbWFpbCI6InMubG9zYWRhQGtsaWtlbmVyZ3kuY29tIiwiZXhwIjoxNzU0NDg0NjQyLCJpc3MiOiJuZXUuY29tLmNvIiwiYXVkIjoibmV1LmNvbS5jbyJ9.zEkmI0uxsx4s0Bhh7rBv0hSrBJxr0zYl4CAbwbxcYXY"
    }

    # Cuerpo de la petición (payload)
    payload = {
        "Sic_codes": [sic_code],
        "From": from_date,
        "To": to_date
    }

    # Realizamos la petición POST
    response = requests.post(url, json=payload, headers=headers)

    # Verificamos el estado de la respuesta
    if response.status_code == 200:
        # Convertimos la respuesta a formato JSON
        data = response.json()
        
        # Validar si la variable 'data' contiene valores o está vacía
        if not data or len(data[0]['data']) < 24:
            sic_code = sic_code
            data = [{'date': f'{date}T{hour:02}:00:00', 'cons': -10000} for hour in range(24)]
        else:
            # Extraer el valor de 'sic_code'
            sic_code = data[0]['sic_code']
            # Extraer la lista de diccionarios asociada a 'data'
            data = data[0]['data']
            # Garantizar que la lista 'data' contenga 24 datos
            while len(data) < 24:
                data.append({'date': f'{date}T{len(data):02}:00:00', 'cons': -10000})

        df = pd.DataFrame(data)

        # Renombrar las columnas a 'Fecha' y 'Consumo'
        df = df.rename(columns={'date': 'Fecha', 'cons': 'Consumo(kWh)'})

        # Convertir la columna 'Fecha' a tipo datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'].str.replace('T', ' '))

        # Ordenar los registros de la fecha más antigua a la más reciente
        df = df.sort_values(by='Fecha')

        # Transponer el dataframe y eliminar la primera fila
        DatosFrontera = df.transpose().iloc[1:].reset_index(drop=True)

        # Agregar columnas adicionales
        DatosFrontera.insert(0, 'CODIGO SIC FRONTERA DDV', sic_code)
        DatosFrontera.insert(1, 'CODIGO SIC FRONTERA COMERCIAL', '')
        DatosFrontera.insert(2, 'tipoMedidor', 'Principal')
        DatosFrontera.insert(3, 'FECHA', df['Fecha'].iloc[0].strftime("%d/%m/%Y"))
        
        # Reemplazar los nombres de las columnas del dataframe 'DatosFrontera' comenzando desde la columna 5
        for i in range(4, 28):
            DatosFrontera.columns.values[i] = f'HORA{i-4:02}'

        # Agregar una columna llamada 'Total' donde se sumen los valores numéricos de la columna 4 a la 29
        DatosFrontera['Total'] = DatosFrontera.iloc[:, 4:29].sum(axis=1)

        # Limitar el número de columnas a 29 y mantener los nombres de las columnas
        Frontera = DatosFrontera.loc[:, DatosFrontera.columns[:29]]

        # Create a new variable called Esteban to store the value of current_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        Esteban = current_time

        return Frontera
    else:
        print("Error en la solicitud:")
        print(f"Código: {response.status_code}")
        print(response.text)
        return None
