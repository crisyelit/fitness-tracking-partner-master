from django.urls import path
from .views import (UserView, )


app_name = 'api_accounts'
urlpatterns = [
    path('me', UserView.as_view()), 
]
