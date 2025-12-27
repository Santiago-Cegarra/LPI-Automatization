from playwright.sync_api import sync_playwright


class CallScraper:
    def __init__(self, user_data_dir: str):
        self.user_data_dir = user_data_dir

    def init_scraper(self):
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=False
            )  # False for debug
            page = browser.new_page()
            page.goto("https://playwright.dev/python/")
            print(page.title())
            browser.close()
