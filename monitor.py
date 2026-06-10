import os
import pandas as pd
from datetime import datetime
from config import STORES
from playwright.sync_api import sync_playwright

FILE = "history.csv"

def init():
    if not os.path.exists(FILE):
        pd.DataFrame(columns=["时间","门店","评分"]).to_csv(FILE, index=False)

def save(name, score):
    df = pd.read_csv(FILE)
    df = pd.concat([df, pd.DataFrame([{
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "门店": name,
        "评分": score
    }])])
    df.to_csv(FILE, index=False)

def fetch(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)

        try:
            el = page.query_selector(".brief-info .score")
            if el:
                return el.inner_text().strip()
        finally:
            browser.close()

    return None

def run():
    init()

    for s in STORES:
        score = fetch(s["url"])
        print(s["name"], score)
        save(s["name"], score)

if __name__ == "__main__":
    run()
