from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from .forms import AccountForm, TransactionForm
from .models import Account, JournalEntry, Transaction

class ChartOfAccountsView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'ledger/account_list.html'


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm

    

class TransactionsView(LoginRequiredMixin, ListView):
    model = Transaction


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['description','transaction_date']

    
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

def post_transaction(request, slug):
    """Get transaction and Post the journal entries to the accounts
        
    """
    transaction = Transaction.objects.filter(slug=slug).first()
    transaction.post_transaction()

    return redirect('transaction-detail', transaction.slug)