from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import ACCOUNT_TYPES, DEBIT_CREDIT

class TransactionForm(forms.ModelForm):
    description = forms.CharField(required=True, label='Transaction Details')

    class Meta:
        model = Transaction
        fields = ['description',]


class AccountForm(forms.ModelForm):
    account_number = forms.CharField(required=True, label='Account Number')
    description = forms.CharField(required=True)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES, label="Account Type")
    natural_balance = forms.ChoiceField(choices=DEBIT_CREDIT, label="Natural Balance")

    class Meta:
        model = Account
        fields = ['account_number', 'description', 'account_type', 'natural_balance',]

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
