from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView
                                       )

from .views import SignUpView, ProfileView, ActivateAccount, UserUpdateView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', SignUpView.as_view(), name="register"),
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                                        email_template_name="mailing/password_reset_email.html",
                                                        success_url=reverse_lazy("accounts:password_reset_done")),
         name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",
                                                                     success_url=reverse_lazy('accounts:password_reset_complete')),
         name="password_reset_confirm"),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name="password_reset_complete"),


    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/edit', UserUpdateView.as_view(), name="profile_edit"),
    path('activate/<uidb64>/<token>/',
         ActivateAccount.as_view(), name='activate'),
]
