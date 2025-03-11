from django.urls import path
from .views import (post_transaction,
    AccountCreateView, 
    AccountDetailView, ChartOfAccountsView, 
    JournalEntriesView, 
    TransactionCreateView, TransactionDetailView, TransactionsView
    )

urlpatterns = [
    path('', ChartOfAccountsView.as_view(), name='accounts'),
    path('account/create/', AccountCreateView.as_view(), name='create-account'),
    path('account/<slug:slug>/', AccountDetailView.as_view(), name='account-detail'),
    path('journal/', JournalEntriesView.as_view(), name='journal'),
    path('journal/<journal_type>/', JournalEntriesView.as_view(), name='filtered-journal'),
    path('transactions', TransactionsView.as_view(), name='transactions'),
    path('transaction/<slug:slug>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/create', TransactionCreateView.as_view(), name='create-transaction'),
    path('transaction/post/<slug:slug>/', post_transaction, name='post-transaction')
]
