"""bookthird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar
from orders.views import admin_order_detail, get_pdf_admin
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('admin/orders/custom/<int:order_id>/', admin_order_detail, name="admin_order_detail"),    # url for custom order detail page
    path('admin/orders/invoice/<int:order_id>/', get_pdf_admin, name='get_pdf_admin'),
    path('rosetta/', include('rosetta.urls')),
    path('', include('cart.urls')),
    path('', include('coupon.urls')),
    path('', include('shop.urls')),
    path(_('order/'), include('payments.urls')),
    path(_('order/'), include('orders.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

)

if settings.DEBUG:
#   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


