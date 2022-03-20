from django.contrib import admin
from django.urls import path, include, reverse_lazy
from .views import (DashboardView, )

app_name = 'dashboard'
urlpatterns = [
	path('', DashboardView.as_view(), name="index"),

	path('training/', include('apps.training.urls')),
]
