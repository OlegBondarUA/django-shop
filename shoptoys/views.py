from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Product


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'categories': Category.objects.all(),
            'products': Product.objects.all(),
        }