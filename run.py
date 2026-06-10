from scraper.fetcher import fetch_page
from scraper.parser import parse_books
from scraper.parser import get_next_page
from scraper.storage import init_db, save_books
from api.app import app
from apscheduler.schedulers.background import BackgroundScheduler
import time

def scrape():
    print("Starting scrape...")
    url = "http://books.toscrape.com"
    page = 1

    while url:
        print(f"Scraping page {page}...")
        html = fetch_page(url)
        if html is None:
            print("Fetch failed, stopping.")
            break
        books = parse_books(html)
        count = save_books(books)
        print(f"Page {page}: saved {count} new books")

        url = get_next_page(html, url)
        page += 1
        time.sleep(1)

if __name__ == "__main__":
    init_db()
    scrape()

    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape, "interval", hours=6)
    scheduler.start()

    app.run(port=5001)