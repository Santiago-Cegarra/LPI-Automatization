import pandas as pd

def cargar_datos(archivo='.\src\liks.xlsx', sheet='Florida'):
    df = pd.read_excel(archivo, sheet_name=sheet, header=0, skiprows=range(1, 153))
    df[["NOMBRE", "APELLIDO"]] = df["NOMBRE COMPLETO"].str.split(pat=" ", n=1, expand=True)
    df[["CALLE", "CIUDAD", "ESTADO_ZIP"]] = df["DIRECCION"].str.split(pat=",", expand=True)
    df["ESTADO_ZIP"] = df["ESTADO_ZIP"].str.strip()
    df[["ESTADO", "ZIP"]] = df["ESTADO_ZIP"].str.split(pat=" ", n=1, expand=True)
    df['BDAY'] = pd.to_datetime(df["F.NACIMIENTO "], errors='coerce').dt.strftime('%m/%d/%Y')
    df['BDAYC'] = pd.to_datetime(df["Fecha NacimientoC"], errors='coerce').dt.strftime('%m/%d/%Y')

    df = df.drop(columns=["NOMBRE COMPLETO", "DIRECCION", "ESTADO_ZIP", "F.NACIMIENTO ", "Fecha NacimientoC"])

    personas = df.to_dict('records')
    return personas

print(cargar_datos())    
