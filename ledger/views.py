from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from .forms import AccountForm, TransactionForm
from .models import Account, JournalEntry, JournalType, Transaction

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
    # model = JournalEntry
    template_name = 'ledger/journal_entry_list.html'

    def get_queryset(self):
        if "journal_type" in self.kwargs.keys():            
            journal_type_key = self.kwargs["journal_type"].upper()
            journal = JournalEntry.objects.filter(journal_type=journal_type_key)
        else:
            journal = JournalEntry.objects.all()
        return journal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "journal_type" in self.kwargs.keys():
            context["journal_type"] = JournalType.objects.filter(code=self.kwargs["journal_type"].upper())[0].description
        else:
            context["journal_type"] = JournalType.objects.filter(code="GJ")[0].description
        return context

def default_journal(request):
    return filtered_journal(request, 'GJ')  # General Journal

def filtered_journal(request, journal_type):
    journalType = JournalType.objects.filter(code=journal_type).first()
    entries = JournalEntry.objects.filter(journal_type = journalType).order_by('transaction')
    context = {
        'journal_type': journalType.description,
        'object_list': entries,
    }
    return render(request, 'ledger/journal_entry_list.html', context)

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