from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'company'

router = DefaultRouter()

router.register('', views.CompanyView)

urlpatterns = [
    path('', include(router.urls)),
]
