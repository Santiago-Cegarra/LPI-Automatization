# Automated Form Filler

> Automatización de formularios web utilizando Playwright y datos desde Excel

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/python/)

## Descripción

Esta es una herramienta de automatización desarrollada para optimizar el flujo de trabajo en una compañia de seguros medicos (LPI), con el llenado automático de formularios web del portal de seguros con información de clientes almacenada en archivos tipo Excel.
Este proyecto personal nacio de la necesidad de reducir el tiempo dedicado a tareas repetitivas de ingreso manual de datos, permitiendo procesar multiples formularios de forma rápida y precisa.

## Instalación y Prerrequisitos
- Python 3.11 o superior
- Google Chrome instalado
### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/Santiago-Cegarra/LPI-Automatization.git
cd tu-repositorio
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Instalar navegadores de Playwright**
```bash
playwright install chromium
```

## Configuración

1. **Crear archivo `settings.py`** en la raíz del proyecto:
```python
# Credenciales
USERNAME = "tu_usuario"
PASSWORD = "tu_contraseña"

# Rutas de archivos
EXCEL_ROUTE = "./src/datos.xlsx"
EXCEL_SHEET = "NombreHoja"

# Directorio de datos del navegador
USER_DATA_DIR = "./chrome_profile"
```

2. **Preparar archivo Excel** con las siguientes columnas:
   - NOMBRE COMPLETO
   - DIRECCION
   - F.NACIMIENTO
   - NUMERO TLF
   - (Otras columnas según necesidad)

### Ejecución básica
```bash
python main.py
```
### Estructura del proyecto
```
├── src/
│   ├── scraper.py           # Lógica principal de automatización
│   ├── data.py              # Procesamiento de datos de Excel
│   ├── scraper_properties.py # Selectores y URLs
│   └── liks.xlsx            # Archivo de datos
├── settings.py              # Configuración (no incluido)
├── main.py                  # Punto de entrada
└── requirements.txt         # Dependencias
```

### Como funciona el scraper?
```python
# El scraper maneja automáticamente:
# - Campos de texto estándar
# - Autocompletes (Material UI)
# - Dropdowns y selects
# - Checkboxes y radio buttons
# - Validaciones y popups
```
---

⭐ considera darle una estrella!

