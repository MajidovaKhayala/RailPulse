from flask import Flask, render_template, send_file
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import pdfkit
import time

app = Flask(__name__)

def scrape_news():
    try:
        url = 'https://www.railwaygazette.com/news'  # Buranı real xəbər mənbəyi ilə əvəz edin
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='news-article')  # Selektoru sayta uyğun dəyişdirin
        news_list = []
        for article in articles:
            title = article.find('h2').text if article.find('h2') else 'Başlıq tapılmadı'
            news_list.append({'title': title})
        return news_list[:10]  # İlk 10 xəbəri götür
    except requests.RequestException as e:
        print(f"Scraping xətası: {e}")
        return [{'title': 'Xəbərlər yüklənə bilmədi'}]

@app.route('/')
def index():
    news_list = scrape_news()
    return render_template('index.html', news=news_list)

@app.route('/export')
def export_to_pdf():
    news_list = scrape_news()
    rendered = render_template('pdf_template.html', news=news_list)
    pdf = pdfkit.from_string(rendered, False)
    return send_file(
        BytesIO(pdf),
        attachment_filename='news.pdf',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
