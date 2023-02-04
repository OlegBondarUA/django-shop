from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Product, ProductImages, Brand

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'categories': Category.objects.all(),
            'brands': Brand.objects.all()[0:6],
            'products': Product.objects.all(),
        }
        return context
