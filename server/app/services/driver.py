# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# options = Options()
# options.add_argument("--start-maximized")  # Start maximized
# options.add_argument("--disable-notifications")  # Disable notifications

# def create_driver ():
#     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Path to your Chrome profile (Linux)
chrome_profile_path = "/home/udorakpuenyi/.config/google-chrome-stable_current_amd64"
profile_directory = "UdorAkpuEnyi"  # Replace with your profile name if not "Default"

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flag
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Hide "Chrome is being controlled by automated software"
options.add_experimental_option("useAutomationExtension", False)  # Disable automation extensions

def create_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

