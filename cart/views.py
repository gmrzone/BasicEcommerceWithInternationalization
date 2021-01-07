from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddQuantityForm
from shop.models import Product
from .cart import Cart
from django.views.decorators.http import require_POST
from coupon.forms import CouponCodeForm
from shop.recommander import Recommander

# Create your views here.
# View to add product to cart or update Quantity
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    selected_product = get_object_or_404(Product, id=product_id)
    quantity_form = AddQuantityForm(request.POST)
    if quantity_form.is_valid():
        cd = quantity_form.cleaned_data
        cart.add(selected_product, cd['quantity'], cd['overide'])
    return redirect('cart_detail')

# Cart remove view to remove product from the cart from cart
def cart_remove(request, product_id):
    cart = Cart(request)
    selected_product = get_object_or_404(Product, id=product_id)
    cart.remove(selected_product)
    return redirect('cart_detail')

# Cart Detail View where we can view all items in the cart
def cart_detail(request):
    coupon_form = CouponCodeForm()
    cart = Cart(request)
    cart_products = []
    for item in cart:
        item['quantity_form'] = AddQuantityForm(initial={'quantity': item['quantity'], 'overide': True})
        cart_products.append(item['product'])
    r = Recommander()
    suggested_products = r.suggest_products(cart_products, 3)
    context = {'cart': cart, 'coupon_form': coupon_form, 'suggested_products': suggested_products}
    return render(request, 'cart/cart_detail.html', context)

