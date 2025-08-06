import requests
from bs4 import BeautifulSoup

def scrape_railway_news():
    sources = [
        {
            "url": "https://www.railwaygazette.com/news/",
            "container": {"class_": "news-list__item"},
            "title": {"tag": "h2"},
            "summary": {"tag": "p"},
            "link": {"tag": "a"}
        }
    ]
    
    all_news = []
    for source in sources:
        try:
            response = requests.get(source['url'], timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all(**source['container'])
            
            for article in articles[:3]:  # İlk 3 xəbər
                title = article.find(**source['title'])
                summary = article.find(**source['summary'])
                link = article.find(**source['link'])
                
                if all((title, summary, link)):
                    all_news.append({
                        "title": title.get_text().strip(),
                        "summary": summary.get_text().strip(),
                        "link": link['href'] if link['href'].startswith('http') else source['url'] + link['href']
                    })
        except Exception as e:
            print(f"Xəta: {e}")
            continue
            
    return all_news or [{"title": "Xəbər tapılmadı", "summary": "Daha sonra yenidən cəhd edin", "link": "#"}]



