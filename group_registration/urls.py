from django.urls import path
from . import views

app_name = 'group_registration'

urlpatterns = [
    path('', views.GroupRegistrationListView.as_view(), name='group-registration-list'),
    path('<int:id>/delete/', views.GroupRegistrationDestroyView.as_view(), name='delete-group-registration'),
    path('create/', views.CreateGroupRegistrationView.as_view(), name='create-group-registration'),
    path('<int:id>/change-status/', views.GroupRegistrationUpdateStatusView.as_view(), name='update-group-registration-status'),
    path('<int:id>/', views.GroupRegistrationRetrieveView.as_view(), name='group-registration-by-id'),
    path('<int:id>/update/', views.UpdateGroupRegistrationView.as_view(), name='update-group-registration-update'),
    path('<int:id>/bind/<int:child_contract_id>', views.GroupRegistrationBindChildContractsView.as_view(), name='bind-child-to-group-registration'),
]
