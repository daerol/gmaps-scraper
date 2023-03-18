from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

PROXIES = [
    "http://proxy1_ip:proxy1_port",
    "http://proxy2_ip:proxy2_port",
    # ... add more proxies as needed ...
]

def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = [line.strip() for line in file]
    return proxies

def create_chrome_options():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless=new")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent={UserAgent().random}')
    return options