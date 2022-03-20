from django.contrib import admin
from django.urls import include, path, reverse_lazy

from . import views

app_name = 'training'
urlpatterns = [
	path('', views.TainingHomeView.as_view(), name="trainig_index"),


	## COACH
	path('coach/routine/', views.RoutineListView.as_view(), name="routine_list"),
	path('coach/routine/<slug:slug>/', views.RoutineDetailView.as_view(), name="routine_detail"),
	path('coach/routine/<slug:slug>/day/create', views.DayRoutineCreateView.as_view(), name="day_routine_create"),
	path('coach/routine/<slug:slug>/day/<slug:public_id>/edit', views.DayRoutineUpdateView.as_view(), name="day_routine_update"),
	path('coach/routine/<slug:slug>/edit', views.RoutineUpdateView.as_view(), name="routine_update"),
	path('coach/routine/<slug:slug>/delete', views.RoutineDeleteView.as_view(), name="routine_delete"),
	path('coach/routine/create', views.RoutineCreateView.as_view(), name="routine_create"),

	path('coach/exercise/', views.ExerciseListView.as_view(), name="exercise_list"),
	path('coach/exercise/<slug:slug>/edit', views.ExerciseUpdateView.as_view(), name="exercise_update"),
	path('coach/exercise/<slug:slug>/delete', views.ExerciseDeleteView.as_view(), name="exercise_delete"),
	path('coach/exercise/create', views.ExcerciseCreateView.as_view(), name="exercise_create"),

	path('coach/customer/', views.CustomerListView.as_view(), name="customer_list"),
	path('coach/customer/<slug:slug>/', views.CustomerRoutineCreateView.as_view(), name="customer_routine_create"),
	path('coach/customer/<int:pk>/edit', views.CustomerRoutineUpdateView.as_view(), name="customer_routine_edit"),

	path('coach/calendar/', views.CalendarView.as_view(), name="training_calendar"),

	## CUSTOMER
	path('routine/', views.CustomerRoutineListView.as_view(), name="customer_routine_list"),
	path('training-with-you/', views.CustomerTrainingWithYouView.as_view(), name="customer_training_with_you"),

	path('routine/<int:pk>/cancel', views.CustomerRoutineCancelView.as_view(), name="customer_routine_cancel"),

	
]


