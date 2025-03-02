from django.urls import path
from . import views

app_name = 'sick_leave'

urlpatterns = [
    path('', views.SickLeaveListView.as_view(), name='sick-leave-list'),
    path('<int:id>/', views.SickLeaveRetrieveDestroyView.as_view(), name='sick-leave-detail'),
    path('create/', views.CreateSickLeaveView.as_view(), name='create-sick-leave'),
    path('<int:id>/edit/', views.SickLeaveEditView.as_view(), name='sick-leave-edit'),
]
