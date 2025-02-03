from django.urls import path
from . import views

app_name = 'sick_leave'

urlpatterns = [
    path('', views.SickLeaveView.as_view(), name='sick-leave'),
    path('<int:id>/', views.RetrieveSickLeaveView.as_view(), name='sick-leave-by-id'),
    path('create/', views.CreateSickLeaveView.as_view(), name='create-sick-leave'),
    path('<int:id>/delete/', views.SickLeaveDeleteView.as_view(), name='delete-sick-leave'),
]
