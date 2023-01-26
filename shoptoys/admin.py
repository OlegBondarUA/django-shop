from django.contrib import admin
from . models import Category, Product, ProductImages, Cart, CartItem


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Cart)
admin.site.register(CartItem)