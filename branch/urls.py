from django.urls import path
from . import views

app_name = 'branch'

urlpatterns = [
    path('', views.BranchListView.as_view(), name='branch-list'),
    path('create/', views.BranchCreateView.as_view(), name='branch-create'),
    path('<int:id>/', views.BranchRetrieveDestroyView.as_view(), name='branch-detail'),
    path('<int:id>/edit/', views.BranchEditView.as_view(), name='branch-edit'),
]
