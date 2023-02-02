from toyshop.models import Category, Product
import os


def main():
    Category.objects.all().delete()
    Product.objects.all().delete()

    dir_ = '/Users/olegbondar/Python/django-shop/media/image'
    for f in os.listdir(dir_):
        os.remove(os.path.join(dir_, f))

    dir_2 = '/Users/olegbondar/Python/django-shop/media/slide_image'
    for f in os.listdir(dir_):
        os.remove(os.path.join(dir_2, f))


if __name__ == '__main__':
    main()
