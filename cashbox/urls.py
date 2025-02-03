from django.urls import path
from . import views

app_name = 'cashbox'

urlpatterns = [
    path('', views.CashboxListView.as_view(), name='cashbox'),
    path('<int:id>/', views.RetrieveCashboxView.as_view(), name='cashbox-by-id'),
    path('create/', views.CreateCashboxeView.as_view(), name='create-cashbox'),
    path('<int:id>/delete/', views.CashboxDeleteView.as_view(), name='delete-cashbox'),
]
