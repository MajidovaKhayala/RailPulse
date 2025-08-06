from flask import render_template, request, jsonify, send_file
from app.utils.scraper import scrape_railway_news
from app.utils.pdf_generator import create_pdf
from app import app
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_news')
def search_news():
    news = scrape_railway_news()
    return jsonify(news)

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    news_data = request.json
    filename = create_pdf(news_data)
    return send_file(filename, as_attachment=True)
