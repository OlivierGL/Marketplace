from django import forms
import re


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password_confirm = forms.CharField()
    country = forms.CharField(initial='Canada')
    province = forms.CharField(initial='Quebec')
    city = forms.CharField(initial='Montreal')
    street_address = forms.CharField()
    postal_code = forms.CharField()

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != \
                cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')

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

