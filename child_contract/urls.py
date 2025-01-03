from django.urls import path
from . import views

app_name = 'child_contract'


urlpatterns = [
    path('', views.ChildContractView.as_view(), name='child-contract'),
    path('<int:id>/change-status/', views.ChildContractUpdateStatusView.as_view(), name='update-child-contract-status'),
    path('<int:id>/delete/', views.ChildContractDeleteView.as_view(), name='delete-child-contract'),
]
