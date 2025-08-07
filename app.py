from flask import Flask, render_template, request
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

def scrape_news():
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        urls = data["urls"]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    results = []

    try:
        for url in urls:
            driver.get(url)
            time.sleep(7)  # saytı yükləmək üçün gözlə

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
        news_data = scrape_news()
    return render_template("index.html", news_data=news_data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

