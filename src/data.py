import pandas as pd
from settings import EXCEL_ROUTE, EXCEL_SHEET
import unicodedata

def normalizar_texto(texto):
    """Remueve tildes y caracteres especiales"""
    if pd.isna(texto):  # Si es NaN o None
        return ""
    texto = str(texto)  # Convertir a string
    # Normalizar y remover tildes
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(char for char in texto if unicodedata.category(char) != 'Mn')
    return texto

def load_data(archivo=EXCEL_ROUTE, sheet=EXCEL_SHEET):
    df = pd.read_excel(archivo, sheet_name=sheet, header=0, skiprows=range(1, 153))
    df[["NOMBRE", "APELLIDO"]] = df["NOMBRE COMPLETO"].str.split(pat=" ", n=1, expand=True)
    df[["NOMBRE_CON", "APELLIDO_CON"]] = df["Conyuge"].str.split(pat=" ", n=1, expand=True)
    df[["CALLE", "CIUDAD", "ESTADO_ZIP"]] = df["DIRECCION"].str.split(pat=",", expand=True)
    df["ESTADO_ZIP"] = df["ESTADO_ZIP"].str.strip()
    df[["ESTADO", "ZIP"]] = df["ESTADO_ZIP"].str.split(pat=" ", n=1, expand=True)
    df['BDAY'] = pd.to_datetime(df["F.NACIMIENTO "], errors='coerce').dt.strftime('%m/%d/%Y')
    df['BDAYC'] = pd.to_datetime(df["Fecha NacimientoC"], errors='coerce').dt.strftime('%m/%d/%Y')
    df["NUMERO TLF"] = df["NUMERO TLF"].astype(str).str.replace('.0', '', regex=False)
    
    df = df.drop(columns=["NOMBRE COMPLETO", "DIRECCION", "ESTADO_ZIP", "F.NACIMIENTO ", "Fecha NacimientoC", "Conyuge"])
    columnas_texto = ["NOMBRE", "APELLIDO", "NOMBRE_CON", "APELLIDO_CON"]
    for col in columnas_texto:
        df[col] = df[col].apply(normalizar_texto)

    personas = df.to_dict('records')
    return personas