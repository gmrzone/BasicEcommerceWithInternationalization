from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _
urlpatterns = [
    path(_('cart/'), views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name="add_cart"),
    path('cart/remove/<int:product_id>/', views.cart_remove, name="remove_cart")
]