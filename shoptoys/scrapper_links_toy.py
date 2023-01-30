import requests
from bs4 import BeautifulSoup
from queue import Queue
from concurrent.futures import ThreadPoolExecutor


def scrape_toys(url):

    with requests.Session() as session:
        response = session.get(url)
        print('Status ', response.status_code)
        assert response.status_code == 200, "Failed to connect to the website"

    soup = BeautifulSoup(response.content, "html.parser")
    toys = soup.find_all('div', class_="product-description")

    for toy in toys:
        url_toys = toy.find('a', class_="product-title").get('href')

        with open('../toys.txt', 'a') as file:
            file.write(url_toys + '\n')


def main():
    urls = [
        "https://myplay.ua/ru/toys",
        'https://myplay.ua/ru/toys?page=2',
        'https://myplay.ua/ru/toys?page=3',
        'https://myplay.ua/ru/toys?page=4',
        'https://myplay.ua/ru/toys?page=5',
        'https://myplay.ua/ru/toys?page=6',
        'https://myplay.ua/ru/toys?page=7',
        'https://myplay.ua/ru/toys?page=8',
    ]

    q = Queue()
    for url in urls:
        q.put(url)

    with ThreadPoolExecutor(max_workers=5) as executor:
        while not q.empty():
            executor.submit(scrape_toys, q.get())


if __name__ == "__main__":
    main()
