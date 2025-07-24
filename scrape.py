import time
import random
import urllib.parse
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROME_DRIVER_PATH = "./chromedriver.exe"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36",
]

def build_search_url(site: str, query: str) -> str:
    q = urllib.parse.quote_plus(query)
    key = site.lower()
    if key == "amazon":
        return f"https://www.amazon.in/s?k={q}"
    elif key == "flipkart":
        return f"https://www.flipkart.com/search?q={q}"
    elif key == "ajio":
        return f"https://www.ajio.com/search/{q}"
    elif key == "myntra":
        return f"https://www.myntra.com/{q}"
    elif key == "meesho":
        return f"https://www.meesho.com/search?q={q}"
    return site

def human_scroll(driver, pause_min=0.5, pause_max=1.5):
    total_height = driver.execute_script("return document.body.scrollHeight")
    step = random.randint(300, 600)
    for y in range(0, total_height, step):
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(random.uniform(pause_min, pause_max))

def scrape_search(site: str, query: str) -> str:
    url = build_search_url(site, query)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 4))
        human_scroll(driver)
        return driver.page_source
    finally:
        driver.quit()

def extract_product_sections(site: str, html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    key = site.lower()
    if key == "amazon":
        elems = soup.select("div.s-main-slot > div[data-asin][data-asin!='']")
    elif key == "flipkart":
        elems = soup.select("div.cPHDOP.col-12-12")
    elif key == "myntra":
        elems = soup.select("li.product-base")
    elif key == "ajio":
        elems = soup.select("div.rilrtl-products-list__item")
    elif key == "meesho":
        elems = soup.select("div.sc-dkrFOg.ProductListItem__GridCol-sc-1baba2g-0.ieFkkv.kdQjpv")
    else:
        elems = [soup.body] if soup.body else []
    return [str(el) for el in elems]

def clean_body_content(body_content: str) -> str:
    soup = BeautifulSoup(body_content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text("\n")
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

def split_dom_content(dom_content: str, max_length: int = 12000) -> List[str]:
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]