from flask import Flask, render_template, send_file
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import pdfkit
import time

app = Flask(__name__)

def scrape_news():
    try:
        url = 'https://www.porttechnology.org/news/us-port-fees-on-china-ships-to-reshape-trade-routes/'  # Railway Gazette xəbər səhifəsi
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Xəta olarsa istisna atır
        soup = BeautifulSoup(response.text, 'html.parser')

        # Əsas selektor: Railway Gazette üçün
        articles = soup.find_all('h3', class_='title')
        news_list = []
        for article in articles:
            title_tag = article.find('a')
            title = title_tag.text.strip() if title_tag else 'Başlıq tapılmadı'
            news_list.append({'title': title})

        # Universial yanaşma: Əgər əsas selektor işləməsə, digər ümumi teqləri yoxla
        if not news_list:
            # Alternativ selektorlar
            for tag in ['h1', 'h2', 'h3', 'h4']:
                articles = soup.find_all(tag)
                for article in articles:
                    title_tag = article.find('a') or article
                    title = title_tag.text.strip() if title_tag else None
                    if title and len(title) > 10:  # Qısa başlıqlardan qaçmaq üçün
                        news_list.append({'title': title})
                if news_list:
                    break  # İlk uğurlu teqdən sonra dayandır

        return news_list[:10] if news_list else [{'title': 'Xəbərlər tapılmadı'}]
    except requests.RequestException as e:
        print(f"Scraping xətası: {e}")
        return [{'title': 'Xəbərlər tapılmadı'}]

@app.route('/')
def index():
    news_list = scrape_news()
    return render_template('index.html', news=news_list)

@app.route('/export')
def export_to_pdf():
    news_list = scrape_news()
    if not news_list:
        news_list = [{'title': 'Xəbərlər tapılmadı'}]
    rendered = render_template('pdf_template.html', news=news_list)
    pdf = pdfkit.from_string(rendered, False)
    return send_file(
        BytesIO(pdf),
        attachment_filename='news.pdf',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
