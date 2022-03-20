import django_filters
from django import forms
from django.db import models
from .models import Exercise, Routine, Resource, Muscle, Tag

class ExerciseFilterform(forms.ModelForm):
	muscles = forms.MultipleChoiceField(label='Musculos',
		choices=[], required=True, widget=forms.CheckboxSelectMultiple())

	resources = forms.MultipleChoiceField(label='Recursos',
		choices=[], required=True, widget=forms.CheckboxSelectMultiple())

	tags = forms.MultipleChoiceField(label='Tags',
		choices=[], required=True, widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Exercise
		fields = ['muscles', 'tags', 'resources', ]

	def __init__(self, qs=False, *args, **kwargs):
		super().__init__(*args, **kwargs)


		if qs:
			MUSCLES = Muscle.objects.filter(exercise__in=qs).order_by().distinct().values_list('id', 'name')

			RESORUCES = Resource.objects.filter(exercise__in=qs).order_by().distinct().values_list('id', 'name')

			TAGS = Tag.objects.filter(exercise__in=qs).order_by().distinct().values_list('id', 'tag')

			self.fields['muscles'] = forms.MultipleChoiceField(
				choices=(*MUSCLES,), required=True, widget=forms.CheckboxSelectMultiple())

			self.fields['resources'] = forms.MultipleChoiceField(
				choices=(*RESORUCES,), required=True, widget=forms.CheckboxSelectMultiple())

			self.fields['tags'] = forms.MultipleChoiceField(
				choices=(*TAGS,), required=True, widget=forms.CheckboxSelectMultiple())


class ExerciseFilter(django_filters.FilterSet):
	class Meta:
		model = Exercise
		fields = [
			'tags', 
			'muscles',
			'resources']


class RoutineFilterform(forms.ModelForm):

	tags = forms.MultipleChoiceField(label='Tags',
		choices=[], required=True, widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Routine
		fields = ['tags',  ]

	def __init__(self, qs=False, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if qs:
			TAGS = Tag.objects.filter(routine__in=qs).order_by().distinct().values_list('id', 'tag')

			self.fields['tags'] = forms.MultipleChoiceField(
				choices=(*TAGS,), required=True, widget=forms.CheckboxSelectMultiple())


class RoutineFilter(django_filters.FilterSet):
	class Meta:
		model = Routine
		fields = [
			'tags', ]