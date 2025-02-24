from django.urls import path, include
from . import views

app_name = 'branch'

<<<<<<< Updated upstream
=======
router = DefaultRouter()

router.register('', views.BranchView, basename='branch')

>>>>>>> Stashed changes
urlpatterns = [
    path('', views.BranchListView.as_view()),
    path('create/', views.BranchCreateView.as_view()),
    path('<int:id>/', views.BranchRetrieveDestroyView.as_view()),
    path('<int:id>/edit/', views.BranchEditView.as_view()),
]
