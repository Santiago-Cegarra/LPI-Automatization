from playwright.sync_api import sync_playwright
from settings import *
from src.scraper_properties import SELECTORS, URLS
from src.data import load_data
import time


class CallScraper:
    def __init__(self, user_data_dir: str):
        self.user_data_dir = user_data_dir
        self.personas = load_data()
    
    def login(self, page):
        page.fill(SELECTORS["email_input"], USERNAME)
        page.fill(SELECTORS["password_input"], PASSWORD)
        page.click(SELECTORS["submit_button"])
        page.wait_for_url(URLS['2fa'])
    
    def fillData(self, page, persona):
        page.fill(SELECTORS["first_name"], persona['NOMBRE'])
        page.fill(SELECTORS["last_name"], persona['APELLIDO'])
        page.fill(SELECTORS["date_birth"], persona['BDAY'])
        time.sleep(1)
        page.click(SELECTORS["state"])
        page.fill(SELECTORS["state"], EXCEL_SHEET)
        time.sleep(1)
        page.press(SELECTORS["state"], "ArrowDown")
        page.press(SELECTORS["state"], "Enter")
        page.check(SELECTORS["permission"])
        page.click(SELECTORS["first_submit"])
        time.sleep(3)
        page.click("text=Crear una nueva solicitud")

    def addSpouse(self, page, persona):
        page.click("//button[@aria-label='Sí']")
        page.click("button:has-text('Agregar a otro solicitante')")
        page.fill(SELECTORS["first_name"], persona['NOMBRE_CON'])
        page.fill(SELECTORS["last_name"], persona['APELLIDO_CON'])
        page.fill(SELECTORS["date_birth"], persona['BDAYC'])
        page.click("text=Hombre")
        page.click("text=Seleccione")
        page.press("input[aria-label='relationshipToPerson.name']", "Enter")
        page.check(SELECTORS["nossn2"])
        page.click("text=Guardar Persona")
        time.sleep(3)
        page.click("button:has-text('Continuar')")

    def fill_form(self, page, persona):
        page.check(SELECTORS["accept1"])
        page.check(SELECTORS["accept2"])
        page.click(SELECTORS["continue"])
        time.sleep(1)
        page.click("text=Mujer")
        page.check(SELECTORS["nossn1"])
        page.click(SELECTORS["continue"])
        time.sleep(3)
        #direccion
        page.fill(SELECTORS["street"], persona["CALLE"])
        page.fill(SELECTORS["city"], persona["CIUDAD"])
        page.fill(SELECTORS["zip"], persona["ZIP"])
        time.sleep(1)
        page.click(SELECTORS["continue"])
        time.sleep(2)
        if page.locator("text=¿Estás seguro de que su dirección es correcta?").is_visible():
            page.click("button:has-text('Continuar')")
        time.sleep(1)
        page.fill(SELECTORS["phone"], persona["NUMERO TLF"])
        page.click("text=Enviar avisos en papel por correo")
        page.click(SELECTORS["continue"])
        time.sleep(10)
        self.addSpouse(page, persona)



    def init_scraper(self):
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=False ,
                channel="chrome"
            )  # False for debug
            page = browser.new_page()
            page.goto(URLS["start_app"])
            time.sleep(2)
            if page.locator(SELECTORS["email_input"]).is_visible():
                self.login(page) 
            time.sleep(2)
            if page.get_by_text("Iniciar Solicitud"):
                page.click("text=Iniciar Solicitud")
            
            for persona in self.personas:
                self.fillData(page, persona)
                time.sleep(3)
                self.fill_form(page, persona)
            #browser.close()
