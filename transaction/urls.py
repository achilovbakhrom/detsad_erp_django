from django.urls import path
from . import views

app_name = 'transaction'

urlpatterns = [
    path('', views.TransactionView.as_view(), name='transaction'),
    path('<int:id>/', views.RetrieveTransactionView.as_view(), name='transaction-by-id'),
    path('create/', views.CreateTransactionView.as_view(), name='create-transaction'),
    path('<int:id>/delete/', views.TransactionDeleteView.as_view(), name='delete-transaction'),
]
