from bs4 import BeautifulSoup
from datetime import datetime, timezone
import re
from urllib.parse import urljoin

def parse_books(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select("article.product_pod"):
        title_tag = card.select_one("h3 a")
        price = card.select_one("p.price_color")

        if not title_tag:
            continue

        jobs.append({
            "title": clean(title_tag.get("title")),
            "price": parse_price(price.text) if price else None,
            "url": "http://books.toscrape.com/" + title_tag.get("href"),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })

    return jobs

def clean(text: str) -> str:
    return " ".join(text.split())

def parse_price(text: str) -> float | None:
    match = re.search(r"[\d.]+", text)
    return float(match.group()) if match else None

def get_next_page(html: str, current_url: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    next_btn = soup.select_one("li.next a")

    if next_btn:
        return urljoin(current_url, next_btn.get("href"))
    return None