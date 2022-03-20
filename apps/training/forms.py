from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from .custom_fields import ChoiceFieldNoValidation, MultipleChoiceFieldNoValidation
from crispy_forms.layout import Button, Submit, Layout, ButtonHolder, MultiField, Div, Button, HTML, Field
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model

from django.db.models import Q

from .models import (
	Gallery,
	Tag,
	Routine,
	Exercise,
	DayRoutine,
	ExerciseRoutine,
	CustomerRoutine,
	Event,
	Resource,
	Muscle
)

# Base


class BaseCustomerRoutineFormSet(forms.BaseModelFormSet):
	def clean(self):
		if any(self.errors):
			# Don't bother validating the formset unless each form is valid on its own
			return
		routines = []
		active = []
		for form in self.forms:
			routine = form.cleaned_data.get('routine')
			status = form.cleaned_data.get('status')

			if routine in routines:
				raise ValidationError(
					"El cliente debe tener rutinas distintas")
			routines.append(routine)

			if status in active:
				raise ValidationError(
					"El cliente solo debe tener una rutina activa")

			if status == 'active':
				active.append(status)

		return super().clean()


class BaseExerciseRoutineFormSet(forms.models.BaseInlineFormSet):
	def clean(self):
		if any(self.errors):
			# Don't bother validating the formset unless each form is valid on its own
			return

		exercises = []
		for form in self.forms:
			if self.can_delete and self._should_delete_form(form):
				continue

			exercise = form.cleaned_data.get('exercise')
			if exercise in exercises:
				raise ValidationError(
					"La rutina debe tener ejercicios distintos")
			exercises.append(exercise)


# Helpers
class CustomerRoutineFormHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.layout = Layout(
			Div(
				Div(
					Div('routine', css_class='col-12 col-md-6'),
					Div('start_date', css_class='col-12 col-md-3'),
					Div('end_date', css_class='col-12 col-md-3'),
					css_class='form-row'
				),
				css_class='formset_container bg-gray-200 bd rounded-5 mb-4 p-2'
			)
		)


class DayRoutineFormHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.form_tag = False
		self.layout = Layout(
			Div(
				Div('name', css_class='col-12 col-md-8'),
				Div('day', css_class='col-12 col-md-4'),
				css_class='form-row'
			),
		)


class ExerciseRoutineFormHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.disable_csrf = True
		self.form_tag = False
		self.layout = Layout(
			Div(
				Div(
					Field("DELETE"),
					css_class='d-flex justify-content-end'
				),
				Div(
					Div('exercise', css_class='col-12 col-md-4'),
					Div('cycles', css_class='col-12 col-md-2'),
					Div('repetitions', css_class='col-12 col-md-2'),
					Div('duration', css_class='col-12 col-md-2'),
					Div('rest', css_class='col-12 col-md-2'),
					css_class='form-row'
				),
				css_class='formset_container bg-gray-200 bd rounded-5 mb-4 p-2'
			)
		)

# Forms


class Exerciseform(forms.ModelForm):
	# gallery = forms.ImageField(label='Imagenes', required=False, allow_empty_file=True,
	# 						   widget=forms.ClearableFileInput(attrs={'multiple': True}))
	muscles = MultipleChoiceFieldNoValidation(label='Musculos',
		choices=[], required=True, widget=forms.SelectMultiple())

	resources = MultipleChoiceFieldNoValidation(label='Recursos',
		choices=[], required=True, widget=forms.SelectMultiple())

	tags = MultipleChoiceFieldNoValidation(label='Tags',
		choices=[], required=True, widget=forms.SelectMultiple())

	class Meta:
		model = Exercise
		fields = ['name', 'muscles', 'tags', 'warnings', 'exercise_result',
						  'resources', 'description', 'image', 'video']
		labels = {
			'name': 'Nombre',	
			'muscles': 'Musculos',
			'tags': 'Tags',
			'exercise_result': 'Tipo de resultado',
			'warnings': 'Advertencias',
			'resources': 'Recursos',
			'description': 'Descripcion',
			'image': 'Imagen',
			'video': 'video',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		instance = kwargs.get('instance')
		if instance:
			MUSCLES = kwargs.get(
				'instance').muscles.values_list('name', 'name')

			RESORUCES = kwargs.get(
				'instance').resources.values_list('name', 'name')

			TAGS = kwargs.get(
				'instance').tags.values_list('tag', 'tag')

			self.fields['muscles'] = MultipleChoiceFieldNoValidation(
				choices=(*MUSCLES,), required=True, widget=forms.SelectMultiple())

			self.fields['resources'] = MultipleChoiceFieldNoValidation(
				choices=(*RESORUCES,), required=True, widget=forms.SelectMultiple())

			self.fields['tags'] = MultipleChoiceFieldNoValidation(
				choices=(*TAGS,), required=True, widget=forms.SelectMultiple())

		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div(
				Div('name', css_class='col-12 col-md-8'),
				Div('exercise_result', css_class='col-12 col-md-4'),
				css_class='form-row'
			),
			'muscles',
			'warnings',
			'resources',
			'description',
			'tags',
			'image',
			'video',
			ButtonHolder(
				Submit('submit', 'Guardar')
			)
		)

	def clean_muscles(self):
		result = []
		for muscle in self.cleaned_data['muscles']:
			try:
				muscle = Muscle.objects.get(name=muscle.lower())
			except Muscle.DoesNotExist:	
				muscle = Muscle.objects.create(name=muscle.lower())
			
			result.append(muscle)	

		return result

	def clean_resources(self):
		result = []
		for resource in self.cleaned_data['resources']:
			try:
				resource = Resource.objects.get(name=resource.lower())
			except Resource.DoesNotExist:	
				resource = Resource.objects.create(name=resource.lower())
			result.append(resource)

		return result

	def clean_tags(self):
		print(self.cleaned_data['tags'])
		result = []
		for tag in self.cleaned_data['tags']:
			tag, created = Tag.objects.get_or_create(tag=tag.lower())
			result.append(tag)

		return result


class RoutineForm(forms.ModelForm):
	tags = MultipleChoiceFieldNoValidation(label='Tags',
		choices=[], required=True, widget=forms.SelectMultiple())
	class Meta:
		model = Routine
		fields = ['name', 'tags', 'description']
		labels = {
			'name': 'Nombre',
			'tags': 'Tags',
			'description': 'Descripción',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		instance = kwargs.get('instance')
		if instance:

			TAGS = kwargs.get(
				'instance').tags.values_list('tag', 'tag')

			self.fields['tags'] = MultipleChoiceFieldNoValidation(
				choices=(*TAGS,), required=True, widget=forms.SelectMultiple())


		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div(
				Div('name', css_class='col-12 col-md-12'),
				css_class='form-row'
			),
			'tags',
			'description',
			ButtonHolder(
				Submit('submit', 'Guardar')
			)
		)
		
	def clean_tags(self):
		print(self.cleaned_data['tags'])
		result = []
		for tag in self.cleaned_data['tags']:
			tag, created = Tag.objects.get_or_create(tag=tag.lower())
			result.append(tag)

		return result


class DayRoutineForm(forms.ModelForm):
	class Meta:
		model = DayRoutine
		fields = ['name', 'day']
		labels = {
			'name': 'Nombre',
			'day': 'Día',
		}


class ExerciseRoutineForm(forms.ModelForm):

	rest = forms.IntegerField(label='Descanso (Segundos)', widget=forms.NumberInput(attrs={'required': True}))
	class Meta:
		model = ExerciseRoutine
		fields = [
			'exercise',
			'cycles',
			'repetitions',
			'duration',
			'rest',
		]

		labels = {
			'exercise': 'Ejercicio',
			'cycles': 'Series',
			'repetitions': 'Repeticiones',
			'duration': 'Duración (Segundos)',
			'rest': 'Descanso (Segundos)',
		}

		# widgets = {
		# 	'exercise': forms.Select(quer)
		# }

	def __init__(self, user=None, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if user:
			EXCERSISES = Exercise.objects.filter(
				Q(is_default=True) | Q(user=user))

			print(EXCERSISES)
			self.fields['exercise'].queryset = EXCERSISES


class CustomerRoutineForm(forms.ModelForm):

	start_date = forms.DateField(
		widget=forms.TextInput(
			attrs={'type': 'date'}
		)
	)

	end_date = forms.DateField(
		widget=forms.TextInput(
			attrs={'type': 'date'}
		)
	)

	class Meta:
		model = CustomerRoutine
		fields = [
			'routine',
			'start_date',
			'end_date'
		]

		labels = {
			'routine': 'Rutina',
			'start_date': 'Fecha inicio',
			'end_date': 'Fecha fin',
		}

	def __init__(self, user=None, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if user:
			ROUTINES = Routine.objects.filter(user=user)

			print(ROUTINES)
			self.fields['routine'].queryset = ROUTINES

		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div(
				Div('routine', css_class='col-12 col-md-6'),
				Div('start_date', css_class='col-12 col-md-3'),
				Div('end_date', css_class='col-12 col-md-3'),
				css_class='form-row'
			),
			ButtonHolder(
				Submit('submit', 'Guardar')
			)
		)

	def clean(self):

		start_date = self.cleaned_data.get('start_date', None)
		end_date = self.cleaned_data.get('end_date', None)

		if start_date and end_date and start_date > end_date:
			raise forms.ValidationError(
				'La fecha de inicio debe ser menor a la fecha de fin')

		return self.cleaned_data

	def clean_end_date(self):

		start_date = self.cleaned_data.get('start_date', None)
		end_date = self.cleaned_data.get('end_date', None)

		if end_date and start_date == None:
			raise forms.ValidationError('Debes ingresar la fecha de inicio')

		return end_date


class CustomerRoutineEditForm(forms.ModelForm):

	class Meta:
		model = CustomerRoutine
		fields = [
			'status',
		]


# Formset
ExerciseRoutineFormSet = forms.inlineformset_factory(
	DayRoutine, ExerciseRoutine, form=ExerciseRoutineForm, formset=BaseExerciseRoutineFormSet, extra=0, min_num=1, max_num=7, can_delete=True)
