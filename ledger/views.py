from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Account

class ChartOfAccountsView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'ledger/account_list.html'


def create_transaction(request):
    context = {
        'placeholder': 'This is just a placeholder'
    }
    return render(request, 'ledger/create_transaction.html', context)