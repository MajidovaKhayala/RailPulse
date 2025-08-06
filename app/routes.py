# Bu import sətirini yoxlayın (1-ci sətirdə olmalıdır):
from app.utils.scraper import scrape_news  # DƏQİQ BU FORMADA OLMALIDIR

# Funksiya çağırışını yoxlayın (heç bir dəyişiklik etməyə ehtiyac yoxdur):
@main_routes.route('/search_news')
def search_news():
    news = scrape_news()  # Funksiya adı eyni qalmalıdır
    return jsonify(news)

# from flask import Blueprint, render_template, jsonify
# from app.utils.scraper import scrape_railway_news

# main_routes = Blueprint('main', __name__)

# @main_routes.route('/')
# def index():
#     return render_template('index.html')

# @main_routes.route('/search_news')
# def search_news():
#     try:
#         news = scrape_railway_news()
#         return jsonify({"success": True, "news": news})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})


# from flask import Blueprint, render_template, jsonify
# from app.utils.scraper import scrape_railway_news

# main_routes = Blueprint('main', __name__)

# @main_routes.route('/')
# def index():
#     return render_template('index.html')  # Artıq base.html istifadə etmir

# @main_routes.route('/search_news')
# def search_news():
#     news = scrape_railway_news()
#     return jsonify(news)
