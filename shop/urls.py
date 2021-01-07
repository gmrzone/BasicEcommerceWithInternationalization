from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>/', views.home, name='home_category'),
    path('<int:id>/<slug:product_slug>/', views.product_detail, name='product_detail')
]