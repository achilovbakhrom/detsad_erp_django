from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'resources'

router = DefaultRouter()

router.register(r'position', views.PositionView)
router.register(r'reason', views.ReasonView)
router.register(r'department', views.DepartmentView)
router.register(r'payment_type', views.PaymentTypeView)
router.register(r'account', views.AccountView)

urlpatterns = [
    path('', include(router.urls)),
]
