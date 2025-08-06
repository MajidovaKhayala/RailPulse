import requests
from bs4 import BeautifulSoup

# Dinamik mənbə konfiqurasiyası
NEWS_SOURCES = [
    {
        "name": "Railway Gazette",
        "url": "https://www.railwaygazette.com/news/",
        "container_selector": ".news-list__item",
        "title_selector": "h2",
        "summary_selector": "p",
        "link_selector": "a",
        "base_url": "https://www.railwaygazette.com"
    },
    # Əlavə etmək istədiyiniz digər saytlar
    # {
    #     "name": "Example News",
    #     "url": "https://example.com/news",
    #     "container_selector": ".news-item",
    #     "title_selector": "h3.title",
    #     "summary_selector": ".summary",
    #     "link_selector": "a.read-more",
    #     "base_url": "https://example.com"
    # }
]

def scrape_railway_news():
    all_news = []
    
    for source in NEWS_SOURCES:
        try:
            response = requests.get(
                source["url"],
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for article in soup.select(source["container_selector"])[:3]:  # Hər mənbədən max 3 xəbər
                try:
                    title = article.select_one(source["title_selector"]).get_text(strip=True)
                    summary = article.select_one(source["summary_selector"]).get_text(strip=True)
                    link = article.select_one(source["link_selector"])["href"]
                    
                    # Nisbi linkləri tam URL-ə çevir
                    if not link.startswith(('http://', 'https://')):
                        link = source["base_url"] + link
                        
                    all_news.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "source": source["name"]
                    })
                except Exception as e:
                    print(f"{source['name']} xəbər parse xətası: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"{source['name']} skreplənmədi: {str(e)}")
            continue
            
    return all_news or [{"title": "Xəbər tapılmadı", "summary": "Daha sonra yenidən cəhd edin", "link": "#"}]

# import requests
# from bs4 import BeautifulSoup

# CUSTOM_SOURCES = [
#     {
#         "name": "Railway Gazette",
#         "url": "https://www.railwaygazette.com/news/",
#         "container": {"class_": "news-list__item"},
#         "title": {"tag": "h2"},
#         "summary": {"tag": "p"},
#         "link": {"tag": "a", "attr": "href"}
#     },
#     # Öz mənbələrinizi buraya əlavə edin
#     # {
#     #     "name": "ADY Özəl Mənbə",
#     #     "url": "https://corp.ady.az/az/media",
#     #     "container": {"class_": "news-class"},
#     #     "title": {"tag": "h3"},
#     #     "summary": {"tag": "div", "class_": "summary"},
#     #     "link": {"tag": "a", "attr": "data-url"}
#     # }
# ]

# def scrape_railway_news():
#     all_news = []
#     for source in CUSTOM_SOURCES:
#         try:
#             response = requests.get(source["url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             for article in soup.find_all(**source["container"]):
#                 try:
#                     title = article.find(**{"tag": source["title"]["tag"]}).get_text(strip=True)
#                     summary = article.find(**{"tag": source["summary"].get("tag"), 
#                                          "class_": source["summary"].get("class_")}).get_text(strip=True)
#                     link = article.find(**{"tag": source["link"]["tag"]}).get(source["link"]["attr"])
                    
#                     if not link.startswith('http'):
#                         link = source["url"] + link
                        
#                     all_news.append({
#                         "title": title,
#                         "summary": summary,
#                         "link": link,
#                         "source": source["name"]
#                     })
#                 except Exception as e:
#                     print(f"{source['name']} xəbərində xəta: {str(e)}")
#                     continue
                    
#         except Exception as e:
#             print(f"{source['name']} skreplənmədi: {str(e)}")
#             continue
            
#     return all_news or [{"title": "Xəbər tapılmadı", "summary": "Daha sonra yenidən cəhd edin", "link": "#"}]


# import requests
# from bs4 import BeautifulSoup

# def scrape_railway_news():
#     sources = [
#         {
#             "url": "https://www.railwaygazette.com/news/",
#             "container": {"class_": "news-list__item"},
#             "title": {"tag": "h2"},
#             "summary": {"tag": "p"},
#             "link": {"tag": "a"}
#         }
#     ]
    
#     all_news = []
#     for source in sources:
#         try:
#             response = requests.get(source['url'], timeout=10)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             articles = soup.find_all(**source['container'])
            
#             for article in articles[:3]:  # İlk 3 xəbər
#                 title = article.find(**source['title'])
#                 summary = article.find(**source['summary'])
#                 link = article.find(**source['link'])
                
#                 if all((title, summary, link)):
#                     all_news.append({
#                         "title": title.get_text().strip(),
#                         "summary": summary.get_text().strip(),
#                         "link": link['href'] if link['href'].startswith('http') else source['url'] + link['href']
#                     })
#         except Exception as e:
#             print(f"Xəta: {e}")
#             continue
            
#     return all_news or [{"title": "Xəbər tapılmadı", "summary": "Daha sonra yenidən cəhd edin", "link": "#"}]



