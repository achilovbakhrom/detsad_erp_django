from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'employee'

router = DefaultRouter()

router.register('', views.EmployeeView)

urlpatterns = [
    path('', include(router.urls)),
]
