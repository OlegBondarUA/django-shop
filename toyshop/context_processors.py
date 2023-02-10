from django.contrib import messages
from django.shortcuts import reverse
from django.db.transaction import atomic

from .selectors import product_category_selector, product_brand_selector


def toyshop_categories(request):
    return {
        'categories': product_category_selector()
    }


def toyshop_brands(request):
    return {
        'brands': product_brand_selector()
    }
