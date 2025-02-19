from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'child'

urlpatterns = [
    path('', views.ChildListView.as_view()),
    path('<int:id>/', views.ChildRetrieveDestroyView.as_view()),
    path('<int:id>/edit/', views.ChildEditView.as_view()),
]
