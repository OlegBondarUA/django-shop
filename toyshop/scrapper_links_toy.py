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

        with open('/Users/olegbondar/Python/django-shop/toys_2.txt', 'a') as file:
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
    urls_2 = [
        'https://myplay.ua/search?category=0&term=LEGO+DUPLO',
        'https://myplay.ua/search?category=0&term=%D0%9A%D1%83%D0%BA%D0%BB%D1%8B+Rainbow+High',
        'https://myplay.ua/search?category=0&term=LEGO+NINJAGO',
        'https://myplay.ua/search?category=0&term=LEGO+CITY',
        'https://myplay.ua/search?category=0&term=LEGO+Star+Wars',
        'https://myplay.ua/search?category=0&term=LEGO+SUPER+MARIO',
        'https://myplay.ua/search?category=0&term=LEGO+FRIENDS',
        'https://myplay.ua/search?category=0&term=LEGO+Marvel+Super+Heroes',
        'https://myplay.ua/search?category=0&term=LEGO+CLASSIC',
        'https://myplay.ua/ru/brands/gravitrax',
        'https://myplay.ua/ru/brands/lego',
        'https://myplay.ua/ru/brands/cubicfun',
        'https://myplay.ua/ru/brands/brand-hot-wheels',
        'https://myplay.ua/ru/brands/rainbow-high',
        'https://myplay.ua/ru/brands/goojitzu'
    ]

    q = Queue()
    for url in urls_2:
        q.put(url)

    with ThreadPoolExecutor(max_workers=5) as executor:
        while not q.empty():
            executor.submit(scrape_toys, q.get())


if __name__ == "__main__":
    main()
