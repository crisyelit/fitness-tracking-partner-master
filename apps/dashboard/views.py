from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = "dashboard/dashboard.html"

	def get_template_names(self):
		if self.request.user.user_type == 'coach':
			return "dashboard/coach_dashboard.html"
		elif self.request.user.user_type == 'customer':
			return "dashboard/customer_dashboard.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
		