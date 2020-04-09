from django import forms
from . import models


class AddProductForm(forms.ModelForm):
	class Meta:
		model = models.Product
		fields = ['name', 'description', 'quantity', 'price', 'image', 'category']
