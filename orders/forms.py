from django import forms
from .models import Order

class CheckoutOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('created', 'updated', 'paid', 'order_id', 'discount', 'coupon')

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Firstname', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Lastname', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Pincode', 'class': 'form-control'})
        }