from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'employee'


urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee-list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('<int:id>/', views.EmployeeRetrieveDestroyView.as_view(), name='employee-detail'),
    path('<int:id>/edit/', views.EmployeeEditView.as_view(), name='employee-edit'),
]
