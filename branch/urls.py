from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'branch'

router = DefaultRouter()

router.register('', views.BranchView)

urlpatterns = [
    path('', include(router.urls)),
]
