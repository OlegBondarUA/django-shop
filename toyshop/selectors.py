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
