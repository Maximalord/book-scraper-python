# book-scraper-python
book-scraper-python
# 📚 Book Scraper with Python – Web Scraping Project

This project is a Python script that scrapes book data (name, price, rating) from [BooksToScrape](http://books.toscrape.com/) using:

- `requests` for fetching HTML content
- `BeautifulSoup` for parsing and extracting HTML data
- `pandas` for organizing and exporting the data to CSV

---

## 🔧 Features

✅ Genre selection from available categories  
✅ Pagination support (scrapes all pages of the selected genre)  
✅ Extracts:
- Book Title
- Price
- Star Rating

✅ Saves the data into a CSV file `books_full.csv`

---

## 🚀 How to Run

```bash
pip install requests beautifulsoup4 pandas
python book_scraper.py
