from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path('accounts/', views.AccountsFinance.as_view(), name="account-finance-report")
]
