import requests
from parsel import Selector
from tech_news.database import create_news
import time


# Requisito 1
def fetch(url):
    try:
        response = requests.get(
            url, timeout=3, headers={"user-agent": "Fake user-agent"}
        )
        time.sleep(1)
        if response.status_code == 200:
            return response.text
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    elements = selector.css(".entry-title")
    list = []
    for element in elements:
        list.append(element.css("a").xpath("@href").get())
    return list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page = selector.css("a.next::attr(href)").get()
    return next_page


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    news = {
        "url": selector.css("link[rel=canonical]::attr(href)").get(),
        "title": selector.css(".entry-title::text").get().strip(),
        "timestamp": selector.css(".meta-date::text").get(),
        "writer": selector.css(".author a::text").get(),
        "reading_time": int(
            selector.css("li.meta-reading-time::text").get().split()[0]
        ),
        "summary": selector.css(".entry-content p")
        .xpath("string()")
        .get()
        .strip(),
        "category": selector.css(".category-style .label::text").get(),
    }
    return news


# Requisito 5
def get_tech_news(amount):
    url = 'https://blog.betrybe.com'
    url_list = []
    news = []
    content = fetch(url)
    url_list.extend(scrape_updates(content))

    while len(url_list) < amount:
        next_page = scrape_next_page_link(content)
        content = fetch(next_page)
        url_list.extend(scrape_updates(content))

    for url in url_list[:amount]:
        new_url = fetch(url)
        fetch_news = scrape_news(new_url)
        news.append(fetch_news)

    create_news(news)
    return news
