from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChartOfAccountsView.as_view(), name='accounts'),
    path('transaction/create', views.create_transaction, name='create-transaction'),
]
