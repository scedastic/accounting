from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChartOfAccountsView.as_view(), name='accounts'),
    path('journal', views.JournalEntriesView.as_view(), name='journal'),
    path('transactions', views.TransactionsView.as_view(), name='transactions'),
    path('transaction/<slug:slug>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/create', views.TransactionCreateView.as_view(), name='create-transaction'),
]
