# AI-Powered E-commerce Web Scraper

This repository contains an AI-driven web scraping application built with Streamlit, Selenium, and LangChain (Ollama LLM). The app enables users to scrape product listings from popular e-commerce sites (Amazon, Flipkart, Myntra, Ajio, Meesho), clean the HTML content, and extract structured data such as product names, prices, and reviews via an LLM-based parser.

## 🚀 Features

- **Multi-site scraping**: Choose between Amazon, Flipkart, Myntra, Ajio, and Meesho.
- **Headless browser**: Uses Selenium with headless Chrome for fast, GUI-free scraping.
- **Human-like behavior**: Randomized user-agents, delays, and scrolling to evade bot detection.
- **Content cleaning**: Extract and clean the page body text with BeautifulSoup.
- **LLM parsing**: Chunked DOM content is sent to Ollama's `gemma3` model via LangChain to extract product name, price, and review in structured Markdown tables.
- **Interactive UI**: Streamlit frontend to select site, enter queries, view scraped text, and trigger analysis.

## 📦 Tech Stack

- **Python 3.8+**
- **Streamlit** for the web interface
- **Selenium** for browser automation
- **BeautifulSoup** for HTML parsing
- **LangChain & LangChain-Ollama** for LLM orchestration
- **Ollama LLM (`gemma3`)** as the language model

## 🔧 Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) matching your Chrome version
- **Optional**: `.env` file with `SBR_WEBDRIVER` if using a remote Selenium server

## 🛠 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/ecommerce-web-scraper.git
   cd ecommerce-web-scraper
   ```

2. **Create a virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download ChromeDriver** and place the executable at the project root or update `CHROME_DRIVER_PATH` in `scrape.py`.

## ⚙️ Configuration

Create a `.env` file at the project root with any of these variables:

```dotenv
# local ChromeDriver path is set in scrape.py:
# CHROME_DRIVER_PATH=./chromedriver.exe
```

## 🚀 Usage

Run the Streamlit app:

```bash
streamlit run main.py
```

1. Select an e-commerce site from the buttons.
2. Enter your search query.
3. Click **Go** to scrape and view the cleaned DOM text.
4. Click **Yes, analyze** to extract a table of product names, prices, and reviews via the Ollama model.

## 📁 Project Structure

```
├── analyser.py         # LLM parsing logic with LangChain & Ollama
├── main.py             # Streamlit app
├── scrape.py           # Selenium-based scraper & cleaning utils
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .env                # Environment variables
```

## 🐞 Troubleshooting

- **`ModuleNotFoundError: No module named 'undetected_chromedriver'`**: Ensure you install only `selenium` and remove stealth imports if not using undetected-chromedriver.
- **Chrome logging noise**: Add `options.add_argument("--log-level=3")` or `options.add_experimental_option("excludeSwitches", ["enable-logging"])` to suppress.
- **CAPTCHAs**: Consider integrating a solver or adding manual intervention when a CAPTCHA appears.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Selenium](https://selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Ollama](https://ollama.ai/)

---

_Happy scraping!_
