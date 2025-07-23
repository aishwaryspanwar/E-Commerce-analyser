import time
import random
import urllib.parse
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
    site = site.lower()
    if site == "amazon":
        return f"https://www.amazon.in/s?k={q}"
    elif site == "flipkart":
        return f"https://www.flipkart.com/search?q={q}"
    elif site == "ajio":
        return f"https://www.ajio.com/search/{q}"
    elif site == "myntra":
        return f"https://www.myntra.com/{q}"
    elif site == "meesho":
        return f"https://www.meesho.com/search?q={q}"
    else:
        return site  # treat as full URL

def human_scroll(driver, pause_min=0.5, pause_max=1.5):
    total_height = driver.execute_script("return document.body.scrollHeight")
    step = random.randint(300, 600)
    for y in range(0, total_height, step):
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(random.uniform(pause_min, pause_max))

def scrape_search(site: str, query: str) -> str:
    url = build_search_url(site, query)
    print("→ Scraping:", url)

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

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(random.uniform(2, 4))
        human_scroll(driver)
        return driver.page_source
    finally:
        driver.quit()

def extract_body_content(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    return str(soup.body or "")

def clean_body_content(body_content: str) -> str:
    soup = BeautifulSoup(body_content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text("\n")
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

def split_dom_content(dom_content: str, max_length: int = 6000) -> list[str]:
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]
