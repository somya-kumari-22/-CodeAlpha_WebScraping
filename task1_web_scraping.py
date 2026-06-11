"""
============================================================
  CodeAlpha Internship — TASK 1: Web Scraping
  Scrapes top headlines from quotes.toscrape.com
  (A free, legal practice website — perfect for internship)
============================================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ── CONFIG ────────────────────────────────────────────────
BASE_URL = "http://quotes.toscrape.com"
OUTPUT_FILE = "scraped_quotes.csv"

# ── SCRAPER FUNCTION ──────────────────────────────────────
def scrape_quotes():
    all_quotes = []
    page = 1

    print("=" * 55)
    print("  CodeAlpha Internship — Task 1: Web Scraping")
    print("=" * 55)

    while True:
        url = f"{BASE_URL}/page/{page}/"
        print(f"\n[*] Scraping Page {page}: {url}")

        response = requests.get(url)

        # Stop if page not found
        if response.status_code != 200:
            print(f"[!] Page {page} not found. Stopping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        # Stop if no quotes on page
        if not quotes:
            print("[!] No more quotes found.")
            break

        for quote in quotes:
            text   = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags   = [t.get_text(strip=True)
                      for t in quote.find_all("a", class_="tag")]

            all_quotes.append({
                "Quote"  : text,
                "Author" : author,
                "Tags"   : ", ".join(tags)
            })
            print(f"    ✔ \"{text[:60]}...\" — {author}")

        # Check if Next button exists
        next_btn = soup.find("li", class_="next")
        if not next_btn:
            print("\n[✓] Reached last page.")
            break

        page += 1
        time.sleep(1)   # polite delay between requests

    return all_quotes

# ── SAVE TO CSV ───────────────────────────────────────────
def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\n[✓] Data saved to '{OUTPUT_FILE}'")
    print(f"    Total quotes scraped: {len(df)}")
    print("\nSample Data:")
    print(df.head(5).to_string(index=False))
    return df

# ── BASIC ANALYSIS ────────────────────────────────────────
def basic_analysis(df):
    print("\n" + "=" * 55)
    print("  BASIC ANALYSIS")
    print("=" * 55)

    print(f"\nTotal Quotes   : {len(df)}")
    print(f"Unique Authors : {df['Author'].nunique()}")

    print("\nTop 5 Most Quoted Authors:")
    print(df['Author'].value_counts().head(5).to_string())

    # Flatten all tags
    all_tags = []
    for tags in df["Tags"].dropna():
        all_tags.extend([t.strip() for t in tags.split(",") if t.strip()])

    tag_series = pd.Series(all_tags)
    print("\nTop 10 Most Common Tags:")
    print(tag_series.value_counts().head(10).to_string())

# ── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    data = scrape_quotes()

    if data:
        df = save_to_csv(data)
        basic_analysis(df)
    else:
        print("[!] No data scraped. Check your internet connection.")

    print("\n" + "=" * 55)
    print("  Task 1 Complete! Upload scraped_quotes.csv")
    print("  to your GitHub repo: CodeAlpha_ProjectName")
    print("=" * 55)
