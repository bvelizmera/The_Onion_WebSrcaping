""" Scrip that scrapes data from the Onion website."""

import requests as req
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import json

class OnionError(Exception):
    """Error acessing the Onion site."""
    pass


def get_article_details(url:str) -> dict:
    """Returns a dict of Onion article data."""
    result = req.get(url)
    if result.status_code >= 400:
        raise OnionError("Could not access URL successfully.")
    
    onion_soup = BeautifulSoup(result.text, features = "html.parser")

    tag_holder = onion_soup.find("div", class_= "taxonomy-post_tag")
    tags = tag_holder.find_all("a") if tag_holder else []

    return {
        "title" : onion_soup.find("h1").get_text(),
        "published" : datetime.fromisoformat(onion_soup.find("time")["datetime"]),
        "tags": [tag.get_text() for tag in tags]
    }

def get_articles_from_page(url:str) -> list[dict]:

    result = req.get(url)

    if result.status_code >= 400:
        raise OnionError("Could not access URL successfully.")

    onion_soup = BeautifulSoup(result.text, features="html.parser")

    links = onion_soup.find_all("h3")
    articles = []
    for l in links:
        articles.append(get_article_details(l.find("a")["href"]))

    return articles


    
    


if __name__ == "__main__":
    # print(get_article_details("https://theonion.com/quentin-tarantino-breaks-three-day-media-silence-1819586098/"))
    all_articles = []
    for i in range(1, 10):
        all_articles.extend( get_articles_from_page(f"https://theonion.com/news/page/{i}"))
    
    
