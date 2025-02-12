from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from .models import Account, JournalEntry, Transaction

class ChartOfAccountsView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'ledger/account_list.html'

class TransactionsView(LoginRequiredMixin, ListView):
    model = Transaction


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
        

class JournalEntriesView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = 'ledger/journal_entry_list.html'

def create_transaction(request):
    context = {
        'placeholder': 'This is just a placeholder'
    }
    return render(request, 'ledger/create_transaction.html', context)