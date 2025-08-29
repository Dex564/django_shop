from django.urls  import path
from . import views

app_name = 'main' # нужен для генерации нейм спейсов, чтобы мы могли обращаться к разным функциям и там ещё чета с шаблонами

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog_all'),
    path('catlog/<slug:category_slug>/', views.CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]


