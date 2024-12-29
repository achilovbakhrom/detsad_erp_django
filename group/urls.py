from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'group'

router = DefaultRouter()

router.register('', views.GroupView)

urlpatterns = [
    path('', include(router.urls)),
]
