from django.urls import path

from . import views

app_name="subscription"

urlpatterns = [
    path('list/', views.SubscriptionListView.as_view(), name="subscription-list"),
    path('<int:id>/', views.SubscriptionRetrieveDestroyView.as_view(), name="subscription-retrieve"),
    path('create/', views.CreateSubscriptionView.as_view(), name="subscription-create"),
]
