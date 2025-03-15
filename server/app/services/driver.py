from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--start-maximized")  # Start maximized
options.add_argument("--disable-notifications")  # Disable notifications

def create_driver ():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
