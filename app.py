import os
import tempfile
from flask import Flask, render_template, request
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

app = Flask(__name__)

def driver_exists(driver_name):
    # Sadə yoxlama: cari qovluqda fayl varmı?
    # Yaxud PATH daxilində axtarış edə bilərik.
    # Burda sadəcə cari qovluqda yoxlayırıq.
    current_dir = os.path.abspath(os.path.dirname(__file__))
    driver_path = os.path.join(current_dir, driver_name)
    return os.path.isfile(driver_path)

def get_webdriver():
    temp_profile = tempfile.mkdtemp()

    # Əvvəlcə chromedriver varsa cəhd et
    if driver_exists("chromedriver.exe"):
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-data-dir={temp_profile}")
        try:
            return webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        except Exception as e:
            print("Chrome driver ilə başlatmaq mümkün olmadı:", e)

    # Əgər Chrome mümkün olmadı, edge driver yoxla
    if driver_exists("msedgedriver.exe"):
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-data-dir={temp_profile}")
        try:
            return webdriver.Edge(executable_path="msedgedriver.exe", options=options)
        except Exception as e:
            print("Edge driver ilə başlatmaq mümkün olmadı:", e)

    # Əgər heç biri yoxdursa
    raise RuntimeError("Heç bir uyğun browser driver tapılmadı!")

def scrape_news():
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        urls = data["urls"]

    driver = get_webdriver()
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
        news_data = scrape_news()
    return render_template("index.html", news_data=news_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
