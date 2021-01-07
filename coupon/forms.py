from django import forms
from django.utils.translation import gettext_lazy as _
class CouponCodeForm(forms.Form):
    code = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': "Coupon Code", 'class': 'form-control'}), label=_('Coupon'))