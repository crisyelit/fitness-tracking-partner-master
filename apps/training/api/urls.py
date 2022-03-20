from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'progress-exercise', views.ExerciseRoutineProgressViewSet, basename='progress_exercise')

# The API URLs are now determined automatically by the router.
app_name = 'api_trainig'
urlpatterns = [
    path('', include(router.urls)),

    path('progress', views.CustomerRoutineProgressListView.as_view(), name='progress'),
    path('coach/progress', views.CoachCustomerRoutineListView.as_view(), name='coach_progress'),

]