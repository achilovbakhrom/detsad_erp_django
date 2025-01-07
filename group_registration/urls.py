from django.urls import path
from . import views

app_name = 'group_registration'

urlpatterns = [
    path('', views.GroupRegistrationView.as_view(), name='group-registration'),
    path('create/', views.CreateGroupRegistrationView.as_view(), name='create-group-registration'),
    path('<int:id>/change-status/', views.GroupRegistrationUpdateStatusView.as_view(), name='update-group-registration-status'),
    path('<int:id>/delete/', views.GroupRegistrationDeleteView.as_view(), name='delete-group-registration'),
]
