from django.urls import path
from . import views

app_name = 'child_contract'


urlpatterns = [
    path('', views.ChildContractListView.as_view(), name='child-contract-list'),
    path('<int:id>/', views.ChildContractRetrieveDestroyView.as_view(), name='child-contract-by-id'),
    path('create/', views.CreateChildContractView.as_view(), name='child-contract-create'),
    path('<int:id>/change-status/', views.ChildContractUpdateStatusView.as_view(), name='child-contract-update-status'),
    path('<int:id>/edit/', views.ChildContractEditView.as_view(), name='child-contract-edit'),
]
