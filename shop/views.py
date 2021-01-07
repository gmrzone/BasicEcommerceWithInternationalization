from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import AddQuantityForm
from django.conf import settings
from .recommander import Recommander
# Create your views here.
def home(request, category_slug=None):
    # set category to none bcoz we want to send category to context and we will get error if category_slug is not provided
    # Get all category and product to display on home page 
    category = None
    products = Product.objects.all().prefetch_related('images')
    categories = Category.objects.all()
    if category_slug:
        # id category slug is passed it means that the user has clicked on a category and we want to show product on that specific category 
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'product/home.html', context)

def product_detail(request, id, product_slug):
    selected_product = get_object_or_404(Product, id=id, slug=product_slug)
    cart_session = request.session.get(settings.CART_SESSION_ID)
    quantity_init = cart_session[str(selected_product.id)]['quantity'] if cart_session.get(str(selected_product.id)) else 0
    quantity_form = AddQuantityForm(initial={'quantity': quantity_init})
    r = Recommander()
    product_suggestions = r.suggest_products([selected_product], max_result=3)
    context = {'selected_product': selected_product, 'add_to_cart': quantity_form, 'product_suggestion': product_suggestions}
    return render(request, 'product/product_details.html', context)
