from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'child'

router = DefaultRouter()

router.register('', views.ChildView)

urlpatterns = [
    path('', include(router.urls)),
]