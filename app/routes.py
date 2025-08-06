from flask import Blueprint, render_template, jsonify, request, send_file
from app.utils.scraper import scrape_railway_news
from app.utils.pdf_generator import create_pdf

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/search_news')
def search_news():
    news = scrape_railway_news()
    return jsonify(news)

@main_routes.route('/export_pdf', methods=['POST'])
def export_pdf():
    news_data = request.json
    filename = create_pdf(news_data)
    return send_file(filename, as_attachment=True)
