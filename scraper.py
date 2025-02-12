import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def main():
    # URL de la página de interés
    url = "https://www.inversionessecurity.cl/consulta-valores-cuota"
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MiScraper/1.0)'
    }
    
    print("Solicitando la página:", url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error al obtener la página, código:", response.status_code)
        return

    # Procesar el HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No se encontró la tabla en el HTML.")
        return

    # Extraer filas de la tabla
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all('td')
        if cells:
            row = [cell.get_text(strip=True) for cell in cells]
            rows.append(row)

    if not rows:
        print("No se extrajeron filas de la tabla.")
        return

    # Crear el DataFrame con los datos extraídos
    df = pd.DataFrame(rows)
    
    # Agregar una columna de Timestamp para forzar cambio en cada ejecución
    df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Agregar la fecha de scrapeo
    df["Fecha de Scrapeo"] = datetime.now().strftime("%Y-%m-%d")

    # Nombre del archivo CSV
    csv_filename = "valores_cuota.csv"
    
    # Si el archivo ya existe, se agregan (append) los nuevos datos sin escribir la cabecera
    if os.path.exists(csv_filename):
        df.to_csv(csv_filename, mode='a', index=False, header=False, encoding="utf-8-sig")
        print("Datos agregados a", csv_filename)
    else:
        df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
        print("Archivo creado:", csv_filename)

if __name__ == '__main__':
    main()
