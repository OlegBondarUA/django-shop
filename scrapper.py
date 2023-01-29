import requests
from bs4 import BeautifulSoup


def scrape_toys(url):

    with requests.Session() as session:
        response = session.get(url)
        print(response.status_code)
        assert response.status_code == 200, "Failed to connect to the website"

    soup = BeautifulSoup(response.content, "html.parser")
    toys = soup.find_all('div', class_="product-description")

    for toy in toys:
        url_toys = toy.find('a', class_="product-title").get('href')
        print(url_toys)


def main():
    url = "https://myplay.ua/ru/toys"
    scrape_toys(url)


if __name__ == "__main__":
    main()
