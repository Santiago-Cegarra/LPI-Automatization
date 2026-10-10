import requests
import unicodedata
from datetime import datetime
from settings import WH_URL


def normalizar_texto(texto):
    if texto is None or str(texto).lower() == 'nan':
        return ""
    texto = str(texto)
    # Normalizar (eliminar acentos)
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(char for char in texto if unicodedata.category(char) != 'Mn') # NOQA


def load_data():
    webhook_url = WH_URL
    print("Conectando con n8n para obtener datos...")
    try:
        response = requests.get(webhook_url)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"Error al obtener datos de n8n: {e}")
        return []

    # Extraemos la lista primero
    if isinstance(raw_data, dict) and "data" in raw_data:
        raw_data = raw_data["data"]

    # ¡Ahora sí mostrará el número real (ej. 100 personas)!
    print(f"¡Éxito! Se recibieron {len(raw_data)} personas para procesar.")

    personas = []
    for item in raw_data:
        persona = {}

        # 1. Separar NOMBRE COMPLETO -> NOMBRE, APELLIDO
        nombre_completo = item.get("NOMBRE COMPLETO", "")
        if nombre_completo:
            partes = str(nombre_completo).split(" ", 1)
            persona["NOMBRE"] = partes[0] if len(partes) > 0 else ""
            persona["APELLIDO"] = partes[1] if len(partes) > 1 else ""
        else:
            persona["NOMBRE"] = ""
            persona["APELLIDO"] = ""

        # 2. Separar Conyuge -> NOMBRE_CON, APELLIDO_CON
        conyuge = item.get("Conyuge", "")
        if conyuge:
            partes = str(conyuge).split(" ", 1)
            persona["NOMBRE_CON"] = partes[0] if len(partes) > 0 else ""
            persona["APELLIDO_CON"] = partes[1] if len(partes) > 1 else ""
        else:
            persona["NOMBRE_CON"] = ""
            persona["APELLIDO_CON"] = ""

        # 3. Procesar DIRECCION -> CALLE, CIUDAD, ESTADO, ZIP
        direccion = item.get("DIRECCION", "")
        if direccion:
            partes_dir = [p.strip() for p in str(direccion).split(",")]
            persona["CALLE"] = partes_dir[0] if len(partes_dir) > 0 else ""
            persona["CIUDAD"] = partes_dir[1] if len(partes_dir) > 1 else ""
            estado_zip_str = partes_dir[2] if len(partes_dir) > 2 else ""
            partes_ez = estado_zip_str.strip().split(" ", 1)
            persona["ESTADO"] = partes_ez[0] if len(partes_ez) > 0 else ""
            persona["ZIP"] = partes_ez[1] if len(partes_ez) > 1 else ""
        else:
            persona["CALLE"] = ""
            persona["CIUDAD"] = ""
            persona["ESTADO"] = ""
            persona["ZIP"] = ""

        # 4. Formatear Fechas (Corregido el espacio en "F. NACIMIENTO")
        for original, nuevo in [("F. NACIMIENTO", "BDAY"), ("Fecha NacimientoC", "BDAYC")]: # NOQA
            fecha_val = item.get(original, "")
            if fecha_val:
                try:
                    fecha_str = str(fecha_val).split('T')[0] 
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                        try:
                            dt = datetime.strptime(fecha_str, fmt)
                            persona[nuevo] = dt.strftime('%m/%d/%Y')
                            break
                        except ValueError:
                            continue
                    else:
                        persona[nuevo] = str(fecha_val)
                except:
                    persona[nuevo] = str(fecha_val)
            else:
                persona[nuevo] = ""

        # 5. Limpiar números y asignar campos directos (Mapeo corregido)
        persona["row_number"] = item.get("row_number")
        persona["NUMERO TLF"] = str(item.get("NUMERO TLF", "")).replace('.0', '')
        persona["ALIEN N"] = str(item.get("ALIEN N Principal", "")).replace('.0', '')
        persona["N DE ALIEN "] = str(item.get("ALIEN N Secundario", "")).replace('.0', '')
        persona["CONYUGE_EMBARAZADA"] = str(item.get("Conyuge Embarazada", "")).strip()
        # 6. Normalizar texto final (acentos, etc.)
        for col in ["NOMBRE", "APELLIDO", "NOMBRE_CON", "APELLIDO_CON"]:
            persona[col] = normalizar_texto(persona.get(col, ""))

        personas.append(persona)
    return personas
