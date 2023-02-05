from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('shop/', views.ProductCatalogView.as_view(), name='oll_shop'),
    path('shop/<slug:slug>/', views.ProductCatalogView.as_view(), name='shop'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product'),
    ]
