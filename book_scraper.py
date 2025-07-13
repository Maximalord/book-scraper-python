import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_genre_url(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        categories = soup.select(".side_categories ul li ul li a")
        genre_map = {}

        print("Available genres:")
        for cat in categories:
            name = cat.text.strip()
            link = cat.get('href')
            genre_map[name.lower()] = base_url + link
            print(f" - {name}")

        selected = input("\nEnter a genre from above (or press Enter to skip): ").strip().lower()
        return genre_map.get(selected, base_url)  # fallback to homepage
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return base_url

def scrape_books_from_url(url):
    book_names = []
    book_pricing = []
    book_ratings = []

    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            titles = soup.find_all('article', class_='product_pod')
            for book in titles:
                # Book title
                name_tag = book.find('h3')
                name = name_tag.a.get('title') if name_tag else 'N/A'
                book_names.append(name)

                # Price
                price_tag = book.find('p', class_='price_color')
                price = price_tag.text.strip() if price_tag else 'N/A'
                book_pricing.append(price)

                # Rating
                rating_tag = book.find('p', class_='star-rating')
                rating = rating_tag.get('class', [])[1] if rating_tag and len(rating_tag.get('class', [])) > 1 else 'N/A'
                book_ratings.append(rating)

            # Check for next page
            next_button = soup.select_one('li.next > a')
            if next_button:
                next_href = next_button['href']
                url = "/".join(url.split("/")[:-1]) + '/' + next_href
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"Error during scraping: {e}")
            break

    return {
        'Book Name': book_names,
        'Book Price': book_pricing,
        'Book Rating': book_ratings
    }

def book_summary():
    base_url = "http://books.toscrape.com/"
    category_url = get_genre_url(base_url)
    data = scrape_books_from_url(category_url)
    return data

# Run and save
data = book_summary()
df = pd.DataFrame(data)
df.to_csv('books_full.csv', index=False)
print(df.head())
