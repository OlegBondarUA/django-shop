from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from . models import Category, Product, ProductImages, Cart, CartItem, Brand


class ImagesInline(admin.TabularInline):
    model = ProductImages
    fields = ('picture', 'image')
    readonly_fields = fields
    extra = 0

    @staticmethod
    def picture(obj):
        return format_html('<img src="{}" style="max-width: 50px">', obj.image.url)


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    inlines = [ImagesInline]
    list_display = ('title', 'old_price', 'price', 'available', 'picture')
    list_filter = ('category', 'brand')
    search_fields = ('title', 'category', 'brand')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': (
                'base_url', 'slug',
                ('title', 'title_en'),
                ('price', 'old_price'),
                ('description',),
                ('image', ),
                ('stock', 'available'),
                ('category',),
                ('brand',)
            )
        }),
    )

    @staticmethod
    def picture(obj):
        return format_html('<img src="{}" style="max-width: 50px">', obj.image.url)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('picture',)

    @staticmethod
    def picture(obj):
        return format_html('<img src="{}" style="max-width: 50px">', obj.image.url)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/toyshop/product/?category__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count}</a>')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/toyshop/product/?brand__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count}</a>')

    @staticmethod
    def picture(obj):
        return format_html('<img src="{}" style="max-width: 50px">', obj.image.url)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ImagesAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Brand, BrandAdmin)
