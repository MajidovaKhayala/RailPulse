import json
import time
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

app = Flask(__name__)

def get_webdriver():
    # Sənə uyğun brauzeri seçmək üçün user-agent yoxlaya bilərsən
    # Burda nümunə üçün Chrome driver seçirik
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print("Chrome driver ilə başlatmaq mümkün olmadı:", e)

    # Əgər Chrome alınmasa, Edge-ə keçə bilərsən:
    try:
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        return driver
    except Exception as e:
        print("Edge driver ilə başlatmaq mümkün olmadı:", e)

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
            time.sleep(7)  # sayt yüklənməsi üçün gözləmə

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
