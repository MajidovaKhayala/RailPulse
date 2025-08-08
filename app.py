from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_browser_driver():
    user_agent = request.headers.get("User-Agent", "").lower()
    # Edge varsa, onu çalışdırmağa çalış, yoxsa Chrome
    if "edg" in user_agent:
        try:
            options = EdgeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver_path = EdgeChromiumDriverManager().install()
            driver = webdriver.Edge(service=EdgeService(driver_path), options=options)
            return driver
        except Exception as e:
            print(f"Edge driver ilə başlatmaq mümkün olmadı: {e}")
            # Fallback olaraq Chrome ilə davam et
    try:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
        return driver
    except Exception as e:
        print(f"Chrome driver ilə başlatmaq mümkün olmadı: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    news_data = None
    if request.method == "POST":
        query = request.form.get("query")
        # news_data-nı query əsasında doldur (və ya sadəcə nümunə kimi)
        news_data = [
            {
                "url": "https://example.com",
                "headlines": [
                    {"title": f"{query} nümunə xəbər 1", "link": "#"},
                    {"title": f"{query} nümunə xəbər 2", "link": "#"},
                ],
            }
        ]
    return render_template("index.html", news_data=news_data)


@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.form.get("url")
    if not url:
        return "URL daxil edin"

    driver = get_browser_driver()
    if not driver:
        return "Browser driver işə düşmədi"

    try:
        driver.get(url)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    news = [item.get_text(strip=True) for item in soup.select("h2")]
    if not news:
        return "Xəbər tapılmadı (empty result). CSS selector-u yoxla."
    
    return "<br>".join(news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
