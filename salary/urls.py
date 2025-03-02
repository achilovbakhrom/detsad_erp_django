from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('', views.SalaryListView.as_view(), name='salary'),
    path('<int:id>/', views.SalaryRetrieveDestroyView.as_view(), name='salary-by-id'),
    path('create/', views.CreateSalaryView.as_view(), name='create-salary'),
]
