from django.urls import path, include
from . import views

app_name="employee_contract"


urlpatterns = [
    path('', views.EmployeeContractListView.as_view(), name="employee-contract-list"),
    path('<int:id>/', views.EmployeeContractRetrieveDestroyView.as_view(), name="employee-contract-retrieve"),
    path('create/', views.HireEmployeeView.as_view(), name="employee-contract-hire"),
    path('<int:id>/hire/', views.ActivateEmployeeContractView.as_view(), name="employee-contract-hire"),
    path('<int:id>/fire/', views.FireEmployeeView.as_view(), name="employee-contract-fire"),
]