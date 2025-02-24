from django.urls import path
from . import views

app_name = 'group'


urlpatterns = [
    path('', views.GroupListView.as_view()),
    path('<int:id>/', views.GroupRetrieveDestroyView.as_view()),
    path('<int:id>/edit/', views.GroupEditView.as_view()),
    path('create/', views.GroupCreateView.as_view()),
]
