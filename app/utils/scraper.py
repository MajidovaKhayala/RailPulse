import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_railway_news():
    sources = [
        {"url": "https://www.railwaygazette.com/news/", "class": "news-list__item"},
        {"url": "https://www.railway-technology.com/news/", "class": "news-article"},
        {"url": "https://www.railjournal.com/news/", "class": "article"}
    ]
    
    all_news = []
    
    for source in sources:
        try:
            response = requests.get(source['url'], timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('div', class_=source['class'])
            
            for article in articles[:5]:
                title = article.find(['h2', 'h3', 'h4'])
                summary = article.find('p')
                link = article.find('a')
                
                if title and summary and link:
                    news_item = {
                        "title": title.text.strip(),
                        "summary": summary.text.strip(),
                        "link": link['href'] if link['href'].startswith('http') else source['url'] + link['href'],
                        "source": source['url'],
                        "date": datetime.now().strftime('%Y-%m-%d')
                    }
                    all_news.append(news_item)
        except Exception as e:
            print(f"Error scraping {source['url']}: {str(e)}")
    
    return all_news[:10]
