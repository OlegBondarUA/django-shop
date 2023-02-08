from random import sample
from django.db.models import Count, F, QuerySet, Avg, Max, Min

from .models import Product, Category, Brand


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


def product_brand_selector() -> QuerySet[Brand]:
    """Return product brands with more than 5 products"""
    return Brand.objects.annotate(num_products=Count('products')).filter(
        num_products__gt=5).order_by('name')


def product_category_selector() -> QuerySet[Category]:
    """Return product categories"""
    return Category.objects.all().order_by('name')
