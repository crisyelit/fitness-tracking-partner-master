from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


# @method_decorator(cache_page(60*60), name='dispatch')
class IndexView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['custom_body_class'] = 'home-body'
		return context

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect(reverse_lazy('dashboard:index'))

		return super().dispatch(request, *args, **kwargs)