from django.views.generic import TemplateView, ListView, DetailView
from .models import Product
from . import selectors
from django.urls import resolve


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'popular_products': selectors.popular_in_shop(),
            'max_rating_products': selectors.max_rating_selector()[0:3],
            'max_rating_products_2': selectors.max_rating_selector()[3:7],
        }
        return context


class ProductCatalogView(ListView):
    template_name = 'shop.html'
    model = Product
    context_object_name = 'products'
    slug_url_kwarg = 'slug'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        self.current_url = resolve(request.path_info).url_name
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')

        if self.current_url == 'shop':
            return queryset.filter(category__slug=slug)

        elif self.current_url == 'brand':
            return queryset.filter(brand__slug=slug)

        return queryset.prefetch_related('category', 'brand')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()

        context |= {
            'total_products': selectors.total_products_selector(products),
            'featured_products': selectors.featured_products_selector()[6:9],
            'all_products': selectors.all_products_selector(),
        }
        return context


class ProductDetailView(DetailView):
    template_name = 'single-product.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    queryset = Product.objects.all().prefetch_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'related_products': selectors.related_products_selector(self.object)
        }
        return context
