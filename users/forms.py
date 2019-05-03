from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Orders

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username','email','firstname','lastname')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username','email')

class customDateInput(forms.DateInput):
    input_type = "date"

class CredentialForm(forms.Form):
    credit_card = forms.IntegerField(required = True)
    cvv = forms.IntegerField(widget = forms.PasswordInput(), required = True)
    expiry = forms.CharField()
    company = forms.CharField(max_length = 200)
    address = forms.CharField(max_length = 200)
    city = forms.CharField(max_length = 100)
    state = forms.CharField(max_length = 100)
    zipcode = forms.IntegerField()
    country = forms.CharField(max_length = 100)