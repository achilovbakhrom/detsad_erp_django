from django.urls import path, include
from . import views

app_name="employee_contract"


urlpatterns = [
    path('list/', views.EmployeeContractsListView.as_view(), name="list"),
    path('<int:id>/', views.RetrieveEmployeeView.as_view(), name="retrieve"),
    path('create/', views.HireEmployeeView.as_view(), name="hire"),
    path('<int:id>/hire/', views.ActivateEmployeeContractView.as_view(), name="hire"),
    path('<int:id>/fire/', views.FireEmployeeView.as_view(), name="fire"),
    path('<int:id>/delete/', views.DeleteEmployeeView.as_view(), name="delete-contract"),
]