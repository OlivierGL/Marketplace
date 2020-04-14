from django import forms
from Users import models as user_models


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = user_models.Address
        fields = ['id', 'country', 'province', 'city', 'street_address', 'postal_code']
