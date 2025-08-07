from flask import Flask, render_template, request
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import tempfile
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

app = Flask(__name__)

def get_webdriver(browser_name="chrome"):
    temp_profile = tempfile.mkdtemp()

    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-data-dir={temp_profile}")
        return webdriver.Chrome(options=options)

    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        profile = webdriver.FirefoxProfile()
        return webdriver.Firefox(firefox_profile=profile, options=options)

    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-data-dir={temp_profile}")
        return webdriver.Edge(options=options)

    else:
        raise ValueError(f"Browser '{browser_name}' dəstəklənmir.")
 
def scrape_news(browser_name="chrome"):
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        urls = data["urls"]

    driver = get_webdriver(browser_name)
    results = []

    try:
        for url in urls:
            driver.get(url)
            time.sleep(7)

            selectors = [
                "h2.headline a",
                "h3.headline a",
                "h2 a",
                "h3 a",
                "article h2 a",
                "div h3 a"
            ]

            elements = []
            for selector in selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    break

            headlines = []
            for el in elements:
                title = el.text.strip()
                link = el.get_attribute("href")
                if title and link:
                    headlines.append({"title": title, "link": link})

            results.append({"url": url, "headlines": headlines})
    finally:
        driver.quit()

    return results


@app.route("/", methods=["GET", "POST"])
def index():
    news_data = []
    if request.method == "POST":
        news_data = scrape_news(browser_name="chrome")  # Və ya firefox, edge
    return render_template("index.html", news_data=news_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
