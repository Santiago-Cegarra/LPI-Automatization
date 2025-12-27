import os
from src.scraper import CallScraper
from src.utils import _create_profile
from settings import *
from src.data import cargar_datos

if not os.path.exists(USER_DATA_DIR):
    _create_profile(path=USER_DATA_DIR)

scraper = CallScraper(user_data_dir=USER_DATA_DIR)
scraper.init_scraper()
