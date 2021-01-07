from django.db import models
from shop.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from coupon.models import CouponCode
import decimal
from django.utils.translation import gettext as _
# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('first name'))
    last_name = models.CharField(max_length=100, verbose_name=_('last name'))
    email = models.EmailField(verbose_name=_("Email"))
    address = models.CharField(max_length=300, verbose_name=_('Address'))
    pincode = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Pincode'))
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('City'))
    paid = models.BooleanField(default=False, verbose_name=_('Paid'))
    order_id = models.CharField(max_length=20, null=True, blank=True, unique=True, verbose_name=_('order ID'))
    braintree_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(CouponCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)

    def get_cart_total(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount_total(self):
        cart_total = self.get_cart_total()
        if self.discount > 0:
            return cart_total - (cart_total * self.discount / decimal.Decimal(100))
        else:
            return cart_total

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        ordering = ('-created',)

    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.quantity * self.price




