from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupon.models import CouponCode

class Cart:

    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session
        self.coupon_id = self.session.get('coupon_id')
        # if cart exist in session then save it in self.cart
        if self.session.get(settings.CART_SESSION_ID, False):
            self.cart = self.session[settings.CART_SESSION_ID]
        else:
        # if cart is not in session the save an empty cart in session
            self.cart = self.session[settings.CART_SESSION_ID] = {}

    @property
    def coupon(self):
        if self.coupon_id:
            coupon = CouponCode.objects.get(id=self.coupon_id)
            return coupon
        return None
    
    def get_discount(self):
        coupon = self.coupon
        if coupon:
            discount = self.get_cart_total() * self.coupon.discount / Decimal(100)
            return discount
        return Decimal(0)

    def price_after_discount(self):
        price = self.get_cart_total() - self.get_discount()
        return price

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, overide_quantity=False):
        # converting product id to str for serializing to JSON as key fo dictionary
        product_id = str(product.id)
        if product_id in self.cart: # if product id is in session cart only change quantity
            if overide_quantity:                 # if overide_quantity is passed as true then assign the new quantity else increment the quantity 
                self.cart[product_id]['quantity'] = quantity
            else:                              
                self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        self.save()                             # save the session

    def remove(self, product):
        # converting product id to str for serializing to JSON as key fo dictionary
        product_id = str(product.id)     
        if product_id in self.cart:   # if product id is in cart then delete that product from cart and save it
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()    # get all product ids from session cart using keys() bcoz we are using product is as key of cart dictionary
        products = Product.objects.filter(id__in=product_ids).prefetch_related('images')   # get all product objects from using product ids from self.cart

        cart = self.cart.copy()    # Create a copy of cart
        # Add product object to cart copy so we vcan use this object in template
        if products:
            for product in products:
                cart[str(product.id)]['product'] = product

            for item in cart.values():    # Iterating over cart values which is a dictionary containing quantity, price and product object added above
                item['price'] = Decimal(item['price'])   # Convert string price back to Decimal
                item['total_price'] = item['quantity'] * item['price']      # create a new data attribute total_price 
                yield item                                                  # Yield items one by one
        else:
            return None                                               

    def __len__(self):
        """count of all items in cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_cart_total(self):
        total = sum(item['quantity'] * Decimal(item['price']) for item in self.cart.values())
        return total
    
    def clear(self):
        # Remove all products from session
        del self.session[settings.CART_SESSION_ID]
        self.save()


