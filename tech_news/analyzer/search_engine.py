from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    news = []
    title = search_news({
        "title": {"$regex": title.lower()}
    })

    for new in title:
        item = new["title"], new["url"]
        news.append(item)

    return news


# Requisito 8
def search_by_date(date):
    try:
        format = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        return [
            (news["title"], news["url"])
            for news in search_news({"timestamp": {"$eq": format}})
        ]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    return [
        (news["title"], news["url"])
        for news in search_news({"category":
                                 {"$regex": f"^{category}$", "$options": "i"}
                                 })
    ]
