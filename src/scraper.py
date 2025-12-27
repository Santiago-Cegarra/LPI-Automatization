from playwright.sync_api import sync_playwright
from settings import *
import time
#Login
emailinput = "//input[@id='username_or_email']"
passinput =  "//input[@id='password']"
submitbtn= "//input[@id='login-submit-button']"
dash_selector = "//span[@id='agent-detail-name']"
dash_url = "https://www.healthsherpa.com/agents/maritza-quinones/clients?_agent_id=maritza-quinones&ffm_applications[agent_archived]=not_archived&ffm_applications[search]=true&term=&renewal=all&desc[]=created_at&agent_id=maritza-quinones&page=1&per_page=50&exchange=onEx&include_shared_applications=false&include_all_applications=false"


class CallScraper:
    def __init__(self, user_data_dir: str):
        self.user_data_dir = user_data_dir
    
    def login(self, page):
        page.fill(emailinput, USERNAME)
        page.fill(passinput, PASSWORD)
        page.click(submitbtn)
        page.wait_for_url("https://www.healthsherpa.com/sessions/two_factor_login")
        page.wait_for_selector(dash_selector, timeout=0)
    
    def init_scraper(self):
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=False ,
                channel="chrome"
            )  # False for debug
            page = browser.new_page()
            page.goto("https://www.healthsherpa.com/person_search?use_case=apply&_agent_id=maritza-quinones")
            time.sleep(2)
            if page.locator(emailinput).is_visible():
                self.login(page) 
            print("Sesion cargada correctamente.") 
            page.pause()
            
            #browser.close()
