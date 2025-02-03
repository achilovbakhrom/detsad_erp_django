from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('', views.SalaryView.as_view(), name='salary'),
    path('<int:id>/', views.RetrieveSalaryView.as_view(), name='salary-by-id'),
    path('create/', views.CreateSalaryView.as_view(), name='create-salary'),
    path('<int:id>/delete/', views.SalaryDeleteView.as_view(), name='delete-salary'),
]
