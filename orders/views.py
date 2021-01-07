from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import CheckoutOrderForm
from django.utils.crypto import get_random_string
from string import ascii_uppercase, digits
from .tasks import order_created_task
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.template.loader import render_to_string
from coupon.forms import CouponCodeForm

# stripe.api_key = settings.STRIPE_SECRET_KEY
# customer = stripe.Customer.create(
#   name='Afzal Saiyed',
#   address={
#     'line1': '510 Townsend St',
#     'postal_code': '98140',
#     'city': 'San Francisco',
#     'state': 'CA',
#     'country': 'US',
#   },
# )

def orderMain(request):
    cart = Cart(request)
    if request.method == "POST":
        checkoutForm = CheckoutOrderForm(data=request.POST)
        if checkoutForm.is_valid():
            instance = checkoutForm.save(commit=False)
            # Generating Order_id
            allowed_char = ''.join(ascii_uppercase + digits)
            order_id = 'ORD' +  get_random_string(length=15, allowed_chars=allowed_char)
            instance.order_id = order_id
            # appling coupon to order
            coupon = cart.coupon
            if coupon:
                instance.coupon = coupon
                instance.discount = coupon.discount
            instance.save()
            for item in cart:
                OrderItem.objects.create(product=item['product'], order=instance, price=item['price'], quantity=item['quantity'])
            # clearing the cart session
            cart.clear()
            # Creating an asynhronous task with celery to send email
            order_created_task.delay(instance.id)
            # Saving order_id to session
            request.session['order_id'] = instance.id
            # redirection to payment page
            return redirect(reverse('payments:payment-process'))
            # return render(request, 'order_success.html', {'order': instance})

    else:
        # intend = stripe.PaymentIntent.create(description="Software development services", shipping={'name': "Afzal Saiyed", 'address': {'line1': '510 Townsend St','postal_code': '98140','city': 'San Francisco','state': 'CA','country': 'US',}} , amount=round(cart.get_cart_total()), currency='inr', metadata={'integration_check': 'accept_a_payment'},)
        checkoutForm = CheckoutOrderForm()
        coupon_form = CouponCodeForm()
        return render(request, 'checkout.html', {'checkout_form': checkoutForm, 'cart': cart, 'coupon_form': coupon_form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'admin/orders/order/detail.html', context)


@staff_member_required
def get_pdf_admin(request, order_id):
  order = get_object_or_404(Order, id=order_id)
  response = HttpResponse(content_type='application/pdf')
  response['Content_deposition'] = f"filename={order.order_id}.pdf"
  html = render_to_string('pdf.html', context={'order': order})
  weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_CSS_DIR + 'pdf.css')])
  return response









