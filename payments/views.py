from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
import braintree
from django.conf import settings
from orders.models import Order
import stripe
from .tasks import order_email_task
stripe.api_key = settings.STRIPE_SECRET_KEY
from shop.recommander import Recommander

# Instantiate a braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

# Create your views here.

def payment_process(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    order_price = order.get_discount_total()
    print(f"{order_price:.2f}")
    if request.method == "POST":
        # retrive nonce 
        nonce = request.POST.get('payment_method_nonce', None)
        # Create and submit Transaction
        result = gateway.transaction.sale({
            'amount': f"{order_price:.2f}",
            'merchant_account_id': 'corecarein',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
             # Get all products for creating recommandation
            products_purchased = [o.product for o in order.items.all()]
            # Mark The order as paid
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            request.session['coupon_id'] = None
            # # Asynchronous task for sending email with invoice attached
            order_email_task.delay(order.id)
            # Create product Recommandation for uprchased product combinations
            
            if len(products_purchased) > 1:
                r = Recommander()
                r.create_recommandation(products_purchased)
            return redirect('payments:payment-success')
        else:
            return redirect('payments:payment-cancelled')
    else:
        # Generate Token and send in context
        client_token = gateway.client_token.generate()
        return render(request, 'process.html', {'client_token':client_token})

def payment_success(request):
    return render(request, 'sucess.html')

def payment_cancelled(request):
    return render(request, 'cancelled.html')

