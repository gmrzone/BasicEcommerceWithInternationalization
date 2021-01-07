from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _
app_name = 'payments'


urlpatterns = [
 path(_('process/'), views.payment_process, name='payment-process'),
 path(_('success/'), views.payment_success, name='payment-success'),
 path(_('cancelled/'), views.payment_cancelled, name='payment-cancelled')

]

