from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .models import CouponCode
from django.utils import timezone
from .forms import CouponCodeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.


    
@require_POST
def apply_coupon(request):
    now = timezone.now()
    coupon_form = CouponCodeForm(data=request.POST)
    if coupon_form.is_valid():
        code = coupon_form.cleaned_data['code']

    try:
        coupon = CouponCode.objects.get(code__iexact=code, is_active=True, valid_from__lte=now, valid_to__gte=now)
        request.session['coupon_id'] = coupon.id
        data = {'status': 'ok', 'discount': coupon.discount, 'code': code}
        
    except:
        request.session['coupon_id'] = None
        data = {'status': 'error', 'discount': 0, 'code': code}
    return JsonResponse(data)

