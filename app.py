from flask import Flask, render_template, send_file
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import pdfkit
import os

app = Flask(__name__)

def scrape_news():
    # Nümunə üçün statik xəbərlər (real URL-lər əlavə edin)
    news_list = [
        {'title': 'Dəmir yolu xəbəri 1', 'content': 'Bu bir nümunə xəbərdir.'},
        {'title': 'Dəmir yolu xəbəri 2', 'content': 'Bu başqa bir xəbərdir.'}
    ]
    # Real scraping üçün:
    # try:
    #     url = 'https://example-railway-news.com'
    #     headers = {'User-Agent': 'Mozilla/5.0'}
    #     response = requests.get(url, headers=headers)
    #     response.raise_for_status()
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     articles = soup.find_all('div', class_='news-article')
    #     news_list = [{'title': article.find('h2').text, 'content': article.find('p').text} for article in articles]
    # except requests.RequestException as e:
    #     print(f"Scraping xətası: {e}")
    #     news_list = []
    return news_list

@app.route('/')
def index():
    news_list = scrape_news()
    return render_template('index.html', news=news_list)

@app.route('/export')
def export_to_pdf():
    news_list = scrape_news()
    rendered = render_template('pdf_template.html', news=news_list)
    # Render üçün wkhtmltopdf konfiqurasiyası
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf') if os.path.exists('/usr/bin/wkhtmltopdf') else None
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    return send_file(BytesIO(pdf), attachment_filename='news.pdf', as_attachment=True)

# Render-də gunicorn tərəfindən istifadə olunur, app.run silinir
