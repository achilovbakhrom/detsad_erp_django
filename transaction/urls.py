from django.urls import path
from . import views

app_name = 'transaction'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction'),
    path('<int:id>/', views.TransactionRetrieveDestroyView.as_view(), name='transaction-by-id'),
    path('create/', views.CreateTransactionView.as_view(), name='create-transaction'),
]
