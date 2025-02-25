from django import forms
from django.forms import widgets
from .models import *
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class TransactionForm(forms.ModelForm):
    description = forms.CharField(required=True, label='Transaction Details')

    class Meta:
        model = Transaction
        fields = ['description',]


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'id': 'floatingInput', 'class': 'form-control form-control-lg', 'placeholder': 'Username'}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'id': 'floatingPassword', 'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
        required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
