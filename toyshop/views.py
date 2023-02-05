from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Product, ProductImages, Brand
from . import selectors


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'categories': Category.objects.all(),
            'brands': Brand.objects.all(),
            'popular_products': selectors.popular_in_shop(),
            'max_rating_products': selectors.max_rating_selector(),
            'max_rating_products_2': selectors.max_rating_selector()[3:],
        }
        return context


class ProductCatalogView(ListView):
    template_name = 'shop.html'
    model = Product
    context_object_name = 'products'
    slug_url_kwarg = 'slug'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        if category:
            queryset = queryset.filter(category__slug=category)
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'categories': Category.objects.all(),
            'brands': Brand.objects.all(),
            'selected_category': self.request.GET.get('category'),
            'selected_brand': self.request.GET.get('brand'),
        }
        return context


class ProductDetailView(DetailView):
    template_name = 'single-product.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'categories': Category.objects.all(),
            'brands': Brand.objects.all(),
            'images': ProductImages.objects.filter(product=self.object),
        }
        return context
