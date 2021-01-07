from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _
app_name = 'orders'

urlpatterns = [
    path(_('checkout/'), views.orderMain, name="checkout"),
    path(_('order-success/'), views.orderMain, name="order_success"),
    path('admin/orders/custom/<int:order_id>/', views.admin_order_detail, name="admin_order_detail")

]