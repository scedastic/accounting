from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChartOfAccountsView.as_view(), name='accounts'),
]
