from random import sample

from django.db.models import Count, QuerySet

from .models import Product, Category, Brand, ProductImages


def popular_in_shop(product_limit: int = 10) -> QuerySet[Product]:
    """Return popular products in shop"""
    return Product.objects.prefetch_related(
        'category', 'brand'
    ).order_by('old_price')[:product_limit]


def max_rating_selector(product_limit: int = 10) -> QuerySet[Product]:
    """Return products with max rating"""
    return Product.objects.prefetch_related(
        'category', 'brand'
    ).order_by('-rating')[:product_limit]


def featured_products_selector() -> QuerySet[Product]:
    """Return featured products"""
    return Product.objects.prefetch_related(
        'category', 'brand'
    ).order_by('-price')


def related_products_selector(product: Product, quantity=4) -> QuerySet[Product]:
    """Return related products"""
    related_product = Product.objects.filter(
        category__id__in=product.category.all()
    ).values_list('id', flat=True)
    random_ids = sample(list(related_product), min(quantity, len(related_product)))
    return Product.objects.filter(id__in=random_ids).prefetch_related(
        'category', 'brand'
    )


def product_brand_selector() -> QuerySet[Brand]:
    """Return product brands with more than 5 products"""
    return Brand.objects.annotate(num_products=Count('products')).filter(
        num_products__gt=5).order_by('name')


def product_category_selector() -> QuerySet[Category]:
    """Return product categories"""
    return Category.objects.all().order_by('name')
