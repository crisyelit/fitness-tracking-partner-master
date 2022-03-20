from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from utils.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views.decorators.http import require_http_methods

from django.contrib import messages


from .forms import SignUpForm, UserUpdateForm
# from girosapp.tasks import sendEmail

# Create your views here.


class SignUpView(CreateView):
	template_name = 'accounts/register.html'
	form_class = SignUpForm
	model = get_user_model()
	success_url = '/accounts/register/'

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		
		messages.success(self.request, '¡Tu usuario fue creado con exito!. Pongase en contacto con el administrador para la activación de su cuenta')

		response = super().form_valid(form)

		# context = {
		# 	'user': form.cleaned_data.get('username'),
		# 	'domain': get_current_site(self.request).domain,
		# 	'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		# 	'token': account_activation_token.make_token(user),
		# }

		# print(user, context)

		# sendEmail.delay('Account confirmation', 'account_activation_email', context, [user.email])

		return response


class ActivateAccount(View):

	def get(self, request, uidb64, token, *args, **kwargs):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = get_user_model().objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.is_email_confirmed = True
			user.save()
			login(request, user)
			messages.success(request, ('Your email have been confirmed.'))
			return redirect('accounts:profile')
		else:
			messages.warning(
				request, ('The confirmation link was invalid, possibly because it has already been used.'))
			return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/dashboard.html'


class UserUpdateView(LoginRequiredMixin, FormView):
	model = get_user_model()
	form_class = UserUpdateForm
	template_name = 'accounts/profile_edit.html'
	success_url = reverse_lazy('accounts:profile_edit')

	def get_form_kwargs(self):
		"""
		Returns the keyword arguments for instantiating the form.
		"""
		kwargs = {
			'initial': self.get_initial(),
			'prefix': self.get_prefix(),
			'instance': self.request.user,

		}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})
		return kwargs

	def form_valid(self, form):
		"""If the form is valid, redirect to the supplied URL."""
		form.save()
		return super().form_valid(form)
