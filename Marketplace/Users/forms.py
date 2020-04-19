import re

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from . import models


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField()


class RatingForm(forms.ModelForm):
  class Meta:
    model = models.Rating
    fields = ['receiver', 'giver', 'rating']


class AddressForm(forms.ModelForm):
  class Meta:
    model = models.Address
    fields = ['country', 'province', 'city', 'street_address', 'postal_code']

  def clean(self):
    cleaned_data = super().clean()

    if 'postal_code' in cleaned_data:
      self.validate_postal_code(cleaned_data['postal_code'])

    for key, value in cleaned_data.items():
      if not value and key in self.initial:
        cleaned_data[key] = self.initial[key]

    return cleaned_data

  def validate_postal_code(self, postal_code):
    # regex for validating postal code for Montreal area only
    regex = r"([H]\d)([ABCEGHJKLMNPRSTVWXYZ]\d){2}$"
    reg_test = re.compile(regex)
    trimmed_postal_code = re.sub(r'[\W_]+', '', postal_code).upper()

    if reg_test.match(trimmed_postal_code) is None:
      self.add_error('postal_code', 'Please enter a valid Montreal area postal code')


class SignupForm(AddressForm):
  username = forms.CharField()
  email = forms.EmailField()
  phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
  first_name = forms.CharField()
  last_name = forms.CharField()
  password = forms.CharField()
  password_confirm = forms.CharField()

  def clean(self):
    cleaned_data = super().clean()

    if 'password' in cleaned_data:
      try:
        validate_password(cleaned_data['password'])
      except ValidationError as err:
        for error_message in err.messages:
          self.add_error('password', error_message)

    if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != \
        cleaned_data['password_confirm']:
      self.add_error('password_confirm', 'Passwords do not match')

    for key, value in cleaned_data.items():
      if not value and key in self.initial:
        cleaned_data[key] = self.initial[key]

    return cleaned_data
