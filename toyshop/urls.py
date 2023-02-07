from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('shop/', views.ProductCatalogView.as_view(), name='all_shop'),
    path('shop/<slug:slug>/', views.ProductCatalogView.as_view(), name='shop'),
    path('shop/brand/<slug:slug>/', views.ProductCatalogView.as_view(), name='brand'),
    path('single-product/<slug:slug>/', views.ProductDetailView.as_view(), name='single'),
    ]
