from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Account

class ChartOfAccountsView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'ledger/account_list.html'