from django.contrib import admin
from django.urls import path, include, reverse_lazy
from .views import (IndexView, )

app_name = 'core'
urlpatterns = [
	path('', IndexView.as_view(), name="index"),
]
