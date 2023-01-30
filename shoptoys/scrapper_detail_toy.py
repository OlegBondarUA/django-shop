import sys
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db.transaction import atomic
from django.utils.text import slugify

from shoptoys.models import Category, Product, ProductImages


TIME_OUT = 10


@atomic
def process(html, url):
    ...


def worker(queue):
    while True:
        url = queue.get()
        print('[WORKING ON]', url)
        try:
            with requests.Session() as session:
                response = session.get(
                    url,
                    allow_redirects=True,
                    timeout=TIME_OUT
                )
                print(response.status_code)

                if response.status_code == 404:
                    print('Page not found', url)
                    break

                assert response.status_code in (200, 301, 302), 'Bad response'

            process(response.text, url)

        except (
                requests.Timeout,
                requests.TooManyRedirects,
                requests.ConnectionError,
                requests.RequestException,
                requests.ConnectTimeout,
                AssertionError
        ) as error:
            print('An error happen', error)
            queue.put(url)

        if queue.qsize() == 0:
            break


def main():
    with open(f'{settings.BASE_DIR}/toys.txt') as file:
        links = file.readlines()

    queue = Queue()

    for url in links:
        queue.put(url)

    worker_number = 10

    with ThreadPoolExecutor(max_workers=worker_number) as executor:
        for _ in range(worker_number):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()
