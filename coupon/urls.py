from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _
app_name = 'coupon'

urlpatterns = [
    path(_('coupons/'), views.apply_coupon, name="apply_coupon"),

]