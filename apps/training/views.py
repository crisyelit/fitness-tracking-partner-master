
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, response
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import RedirectView
from django.utils import timezone

from .filters import ExerciseFilter, ExerciseFilterform, RoutineFilter, RoutineFilterform
from apps.training.forms import (
								 CustomerRoutineForm,
								 Exerciseform,
								 ExerciseRoutineFormHelper,
								 ExerciseRoutineFormSet, RoutineForm,
								 DayRoutineForm, DayRoutineFormHelper, CustomerRoutineEditForm)

from .models import Event, Exercise, Gallery, Routine, DayRoutine, CustomerRoutine, CustomerRoutineProgress

from .mixins import UserIsCoachMixin, CustomerHasTrainingMixin
from .services import CustomerRoutineProgressService


from django.contrib import messages


class TainingHomeView(LoginRequiredMixin, RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		if self.request.user.user_type == 'coach':
			return reverse_lazy('dashboard:training:routine_list')
		elif self.request.user.user_type == 'customer':
			return reverse_lazy('dashboard:training:customer_routine_list')

		return Http404

# COACH VIEWS


class CalendarView(LoginRequiredMixin, UserIsCoachMixin, TemplateView):
	template_name = 'training/coach/calendar.html'


class RoutineCreateView(LoginRequiredMixin, UserIsCoachMixin, CreateView):
	template_name = "training/coach/routine_form.html"
	form_class = RoutineForm
	model = Routine

	def get_success_url(self):
		return reverse_lazy('dashboard:training:routine_detail', kwargs={'slug': self.object.slug})

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class DayRoutineCreateView(LoginRequiredMixin, UserIsCoachMixin, TemplateView):
	template_name = "training/coach/day_routine_form.html"
	form_class = DayRoutineForm
	form_helper = DayRoutineFormHelper
	formset_class = ExerciseRoutineFormSet
	formset_helper = ExerciseRoutineFormHelper

	model = Routine

	def get_object(self, *args, **kwargs):
		try:
			return self.model.objects.get(slug=self.kwargs['slug'], user=self.request.user)
		except self.model.DoesNotExist:
			raise Http404()

	def get(self, *args, **kwargs):
		obj = self.get_object()
		form = self.form_class()
		form_helper = self.form_helper()
		formset = self.formset_class(form_kwargs={'user': self.request.user})
		formset_helper = self.formset_helper()

		return self.render_to_response({'form': form,
										'form_helper': form_helper,
										'formset': formset,
										'formset_helper': formset_helper})

	def post(self, *args, **kwargs):
		obj = self.get_object()
		form = self.form_class(data=self.request.POST)
		form_helper = self.form_helper()
		formset = self.formset_class(data=self.request.POST, form_kwargs={
			'user': self.request.user})
		formset_helper = self.formset_helper()

		# Check if submitted forms are valid
		if form.is_valid() and formset.is_valid():
			day_routine = form.save(commit=False)
			day_routine.user = self.request.user
			day_routine.routine = obj
			day_routine.save()

			for exercise in formset:
				formset_routine = exercise.save(commit=False)
				formset_routine.user = self.request.user
				formset_routine.day_routine = day_routine
				formset_routine.save()

			return redirect(reverse_lazy("dashboard:training:routine_detail", kwargs={'slug': obj.slug}))

		return self.render_to_response({'form': form,
										'form_helper': form_helper,
										'formset': formset,
										'formset_helper': formset_helper})


class DayRoutineUpdateView(LoginRequiredMixin, UserIsCoachMixin, TemplateView):
	template_name = "training/coach/day_routine_form.html"
	form_class = DayRoutineForm
	form_helper = DayRoutineFormHelper
	formset_class = ExerciseRoutineFormSet
	formset_helper = ExerciseRoutineFormHelper

	first_model = Routine
	second_model = DayRoutine

	def get_objects(self, *args, **kwargs):
		try:
			first_obj = self.first_model.objects.get(
				slug=self.kwargs['slug'], user=self.request.user)
			second_obj = self.second_model.objects.get(
				slug=self.kwargs['public_id'], routine=first_obj, user=self.request.user)

			return (first_obj, second_obj)

		except self.first_model.DoesNotExist:
			raise Http404()
		except self.second_model.DoesNotExist:
			raise Http404()

	def get(self, *args, **kwargs):
		_, obj = self.get_objects()
		form = self.form_class(instance=obj)
		form_helper = self.form_helper()
		formset = self.formset_class(instance=obj, form_kwargs={
			'user': self.request.user})
		formset_helper = self.formset_helper()

		return self.render_to_response({'form': form,
										'form_helper': form_helper,
										'formset': formset,
										'formset_helper': formset_helper,
										'object': obj})

	def post(self, *args, **kwargs):
		routine, obj = self.get_objects()
		form = self.form_class(data=self.request.POST, instance=obj)
		form_helper = self.form_helper()
		formset = self.formset_class(data=self.request.POST, instance=obj, form_kwargs={
			'user': self.request.user})
		formset_helper = self.formset_helper()

		# Check if submitted forms are valid
		if form.is_valid() and formset.is_valid():
			day_routine = form.save(commit=False)
			day_routine.user = self.request.user
			day_routine.routine = routine
			day_routine.save()

			instances = formset.save(commit=False)
			for obj in formset.deleted_objects:
				obj.delete()
			for instance in instances:
				instance.user = self.request.user
				instance.day_routine = day_routine
				instance.save()

			formset.save_m2m()

			return redirect(reverse_lazy("dashboard:training:routine_detail", kwargs={'slug': routine.slug}))

		return self.render_to_response({'form': form,
										'form_helper': form_helper,
										'formset': formset,
										'formset_helper': formset_helper,
										'object': obj})


class RoutineUpdateView(LoginRequiredMixin, UserIsCoachMixin, UpdateView):
	template_name = "training/coach/routine_form.html"
	success_url = reverse_lazy('dashboard:training:routine_list')
	form_class = RoutineForm
	model = Routine

	def get_queryset(self):
		return super().get_queryset().filter(user=self.request.user)


class RoutineDeleteView(LoginRequiredMixin, UserIsCoachMixin, DeleteView):
	model = Routine
	success_url = reverse_lazy('dashboard:training:routine_list')
	template_name = "training/coach/routine_confirm_delete.html"

	def get_object(self, *args, **kwargs):
		try:
			return self.model.objects.get(slug=self.kwargs['slug'], user=self.request.user)
		except self.model.DoesNotExist:
			raise Http404()


class RoutineDetailView(LoginRequiredMixin, UserIsCoachMixin, DetailView):
	model = Routine
	template_name = "training/coach/routine_detail.html"

	def get_object(self, *args, **kwargs):
		try:
			return self.model.objects.get(slug=self.kwargs['slug'], user=self.request.user)
		except self.model.DoesNotExist:
			raise Http404()


class RoutineListView(LoginRequiredMixin, UserIsCoachMixin, ListView):
	model = Routine
	paginate_by = 8
	template_name = "training/coach/routine_list.html"

	def get_queryset(self):
		qs = self.model.objects.filter(user=self.request.user).order_by('-created_at')
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = RoutineFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = RoutineFilterform(qs=self.get_queryset())
		return context


class ExcerciseCreateView(LoginRequiredMixin, UserIsCoachMixin, CreateView):
	model = Exercise
	form_class = Exerciseform

	template_name = 'training/coach/exercise_form.html'
	success_url = reverse_lazy('dashboard:training:exercise_list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class ExerciseUpdateView(LoginRequiredMixin, UserIsCoachMixin, UpdateView):
	model = Exercise
	form_class = Exerciseform
	template_name = 'training/coach/exercise_form.html'
	success_url = reverse_lazy('dashboard:training:exercise_list')

	def get_object(self, *args, **kwargs):
		try:
			return self.model.objects.get(slug=self.kwargs['slug'], user=self.request.user)
		except self.model.DoesNotExist:
			raise Http404()


class ExerciseDeleteView(LoginRequiredMixin, UserIsCoachMixin, DeleteView):
	model = Exercise
	success_url = reverse_lazy('dashboard:training:exercise_list')
	template_name = "training/coach/exercise_confirm_delete.html"

	def get_object(self, *args, **kwargs):
		try:
			return self.model.objects.get(slug=self.kwargs['slug'], user=self.request.user)
		except self.model.DoesNotExist:
			raise Http404()


class ExerciseListView(LoginRequiredMixin, UserIsCoachMixin, ListView):
	model = Exercise
	template_name = "training/coach/exercise_list.html"

	def get_queryset(self):
		qs = self.model.objects.filter(user=self.request.user).order_by('-created_at')
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = ExerciseFilter(self.request.GET, queryset=self.get_queryset())
		context['filter_form'] = ExerciseFilterform(qs=self.get_queryset())
		return context


class CustomerListView(LoginRequiredMixin, UserIsCoachMixin, ListView):
	model = get_user_model()
	template_name = 'training/coach/customer_list.html'

	def get_queryset(self):
		return super().get_queryset().filter(user_type="customer", parent=self.request.user, enable_training = True)


class CustomerRoutineCreateView(LoginRequiredMixin, UserIsCoachMixin, CreateView):
	template_name = "training/coach/customer_form.html"
	form_class = CustomerRoutineForm
	success_url = reverse_lazy('dashboard:training:routine_list')
	model = CustomerRoutine
	customer_model = get_user_model()

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_customer()
		if obj.customerOf.active().exists():
			messages.warning(
				request, 'Este usuario ya posee una rutina activa')

			return redirect('dashboard:training:customer_list')

		return super().dispatch(request, *args, **kwargs)

	def get_customer(self, *args, **kwargs):
		try:
			obj =  self.customer_model.objects.get(
				public_id=self.kwargs['slug'])
			return obj
		except self.customer_model.DoesNotExist:
			raise Http404()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['customer'] = self.get_customer()

		return context

	def get_form_kwargs(self):
		"""
		Returns the keyword arguments for instantiating the form.
		"""
		kwargs = {
			'initial': self.get_initial(),
			'prefix': self.get_prefix(),
			'user': self.request.user,

		}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})
		return kwargs

	def form_valid(self, form):
		form.instance.coach = self.request.user
		form.instance.customer = self.get_customer()
		form.instance.status = 'active'
		return super().form_valid(form)

class CustomerRoutineUpdateView(LoginRequiredMixin, UserIsCoachMixin, UpdateView):
	form_class = CustomerRoutineForm
	model = CustomerRoutine
	template_name = 'training/coach/customer_form.html'

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.customer != self.request.user and obj.coach != self.request.user or obj.status == 'canceled':
			raise Http404

		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):

		if self.request.user.user_type == 'customer':
			return reverse_lazy('dashboard:training:customer_routine_list')

		return reverse_lazy('dashboard:training:customer_list')

	def form_valid(self, form):
		form.instance.status = 'active'
		return super().form_valid(form)

# CUSTOMER VIEWS
class CustomerRoutineListView(LoginRequiredMixin, CustomerHasTrainingMixin, TemplateView):
	model = CustomerRoutine
	template_name = 'training/customer/customerroutine_list.html'

	def get_object(self):
		routine = self.request.GET.get('routine', None)
		try:
			if routine:
				return self.model.objects.get(slug=routine, customer=self.request.user)
			else:
				return self.model.objects.filter(customer=self.request.user).order_by('status').first()

		except self.model.DoesNotExist:
			raise Http404()


	def validate_routine_dates(self):
		today = timezone.now().date()
		obj = self.get_object()
		if obj and obj.start_date and obj.end_date:
			return today > obj.start_date and today < obj.end_date 

		return False


	def get(self, *args, **kwargs):
		obj = self.get_object()

		routine_dates  = self.validate_routine_dates() 
		print(routine_dates)

		return self.render_to_response({
										'routine': obj,
										'routine_dates': routine_dates,
										})

class CustomerTrainingWithYouView(LoginRequiredMixin, CustomerHasTrainingMixin, TemplateView):
	template_name = 'training/customer/training_with_you.html'
	model = CustomerRoutine

	service = CustomerRoutineProgressService

	def get_objects(self):

		exercise = self.request.GET.get('exercise', None)
		
		progress_service = self.service(self.request.user)
		validate_customer_routine = progress_service.validate_customer_routine()
		
		if validate_customer_routine.get('code') != 'VALID':
			return validate_customer_routine

		progress = progress_service.get_or_create_day_routine()
		if progress.get('code') == 'INVALID_DAY' or progress.get('code') == 'EMPTY_DAY_ROUTINE':
			return progress

		if exercise:
			exercise = progress_service.set_current_exercise(exercise)
			if exercise.get('code') == 'INVALID_EXERCISE_ROUTINE':
				raise Http404

		day_progress = progress_service.get_day_progress()
		
		return {'customer_routine': progress_service.customer_routine, 'day_progress': day_progress, **progress,}

	def get(self, *args, **kwargs):
		context = self.get_objects()
		print(context)

		return self.render_to_response(context)


class CustomerRoutineCancelView(LoginRequiredMixin, UpdateView):
	form_class = CustomerRoutineEditForm
	model = CustomerRoutine
	template_name = 'training/customer/customerroutine_form.html'

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.customer != self.request.user and obj.coach != self.request.user or obj.status == 'canceled':
			raise Http404

		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):

		if self.request.user.user_type == 'customer':
			return reverse_lazy('dashboard:training:customer_routine_list')

		return reverse_lazy('dashboard:training:customer_list')

	def form_valid(self, form):
		form.instance.status = 'canceled'
		return super().form_valid(form)