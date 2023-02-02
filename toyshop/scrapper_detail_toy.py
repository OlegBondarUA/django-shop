import sys
import random
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from PIL import Image

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db.transaction import atomic
from django.utils.text import slugify

from toyshop.models import Category, Product, ProductImages


TIME_OUT = 10


def upload_image_to_local_media(img_url: str, image_name: str):
    with requests.Session() as session:
        img_response = session.get(img_url, timeout=TIME_OUT)

    with open(f'media/image/{image_name}', 'wb') as img_file:
        img_file.write(img_response.content)
    img = Image.open(f'media/image/{image_name}').convert('RGB')
    img.save(f'media/image/{image_name}.jpg', 'JPEG')


def upload_slide_image_to_local_media(
        img_url: str,
        image_name: str,
        product: Product
):
    with requests.Session() as session:
        img_response = session.get(img_url, timeout=TIME_OUT)

    with open(f'media/slide_image/{image_name}', 'wb') as file:
        file.write(img_response.content)
    img = Image.open(f'media/slide_image/{image_name}').convert('RGB')
    img.save(f'media/slide_image/{image_name}.jpg', 'JPEG')

    ProductImages.objects.create(
        product=product,
        image=f'slide_image/{image_name}.jpg',
        base_url=img_url
    )

    del img_response


@atomic
def process(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        name = soup.find('h1', class_='page-title').text.strip()
        slug = slugify(name)
        description = soup.select('.collapse-inner p')
        description = [p.text.strip() for p in description]
        price = soup.select('.price .price-value')[0].text.replace('\xa0', '').strip()
        img = soup.select(".slider-item")[0].find('img').get('src')
        slide_img = soup.select(".slider-item")
        slide_img = [i.find('img').get('src') for i in slide_img]
        stock = random.randint(3, 100)
        category_name = soup.select('.characteristics-wrap')[0].find_all('a')[1].text.strip()
        category_slug = slugify(category_name)

        img_name = img.split('/')[-1]
        upload_image_to_local_media(img, img_name)

        product = Product.objects.create(
            base_url=url,
            title=name,
            slug=slug,
            description=description,
            price=price,
            image=f'image/{img_name}.jpg',
            stock=stock,
        )

        category, _ = Category.objects.get_or_create(
            slug=category_slug,
            defaults={
                'name': category_name,
                'slug': category_slug
            }
        )
        product.category.add(category)

        for image_url in slide_img:
            image_name = image_url.split('/')[-1]
            upload_slide_image_to_local_media(image_url, image_name, product)

        print('Done', url)

    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Parsing Error', error, exc_tb.tb_lineno, url)


def worker(queue):
    while queue.qsize() > 0:
        url = queue.get()
        print('[WORKING ON]', url)
        try:
            with requests.Session() as session:
                response = session.get(
                    url,
                    allow_redirects=True,
                    timeout=TIME_OUT
                )
                print(response.status_code, '\n')

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


def main():
    with open(f'{settings.BASE_DIR}/toys_2.txt') as file:
        links = file.readlines()

    queue = Queue()

    for url in links:
        queue.put(url.strip())

    worker_number = 10

    with ThreadPoolExecutor(max_workers=worker_number) as executor:
        for _ in range(worker_number):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()
