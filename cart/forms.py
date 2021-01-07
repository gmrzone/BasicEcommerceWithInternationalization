from django import forms
from django.utils.translation import gettext_lazy as _
QUANTITY_CHOISES = [(i, str(i)) for i in range(21)]

class AddQuantityForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOISES, coerce=int, label=_('Quantity'))
    overide = forms.BooleanField(required=False, widget=forms.HiddenInput, initial=False)

