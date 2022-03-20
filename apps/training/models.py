from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from utils.generators import *


def image_directory_path(instance, filename):
	return f'{instance.slug}/{filename}'


def exercise_directory_path(instance, filename):
	return f'exercise/{instance.slug}/{filename}'

# Create your models here.
class Muscle(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=100, unique=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
class Resource(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=100, unique=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
class Gallery(models.Model):

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	image = models.ImageField(
		upload_to=image_directory_path, blank=True, null=True)
	slug = models.SlugField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.slug
class Tag(models.Model):
	tag = models.CharField(max_length=50, unique=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.tag
class Exercise(models.Model):

	LEVEL_CHOICES = (
		('easy', _('Easy')),
		('medium', _('Medium')),
		('hard', _('Hard')),
	)
	EXERCISE_RESULT_CHOICES = (
		('weight', _('Weight')),
		('time', _('Time')),
		('repetitions', _('Repetitions')),
	)

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	name = models.CharField(max_length=200)
	slug = models.SlugField(blank=True, null=True)

	tags = models.ManyToManyField(Tag, blank=True)

	warnings = models.TextField(blank=True, null=True)
	description = models.TextField()

	muscles = models.ManyToManyField(Muscle, blank=True)
	resources = models.ManyToManyField(Resource, blank=True)
	gallery = models.ManyToManyField(Gallery, blank=True)
	level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='easy')

	exercise_result = models.CharField(max_length=11, choices=EXERCISE_RESULT_CHOICES, default='weight')

	is_default = models.BooleanField(default=False)

	image = models.ImageField(
		upload_to=exercise_directory_path, blank=True, null=True)
	video = models.FileField(upload_to=exercise_directory_path, null=True, blank=True,
							 validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
class Event(models.Model):
	"""Model definition for Week."""
	name = models.CharField(max_length=150)
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	slug = models.SlugField(blank=True, null=True)

	description = models.TextField(blank=True, null=True)

	event_type = models.CharField(max_length=20, choices=(
		('routine', 'Routine'), ('meeting', 'Meeting')), default='routine')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
class Routine(models.Model):
	STATUS_CHOICES = (
		('draft', _('Draft')),
		('active', _('Active')),
		('archived', _('Archived')),
	)

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	slug = models.SlugField(blank=True, null=True)
	name = models.CharField(max_length=150, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name if self.name else self.pk
class DayRoutine(models.Model):
	DAY_CHOICES = (
		('monday', _('Monday')),
		('tuesday', _('Tuesday')),
		('wednesday', _('Wednesday')),
		('thursday', _('Thursday')),
		('friday', _('Friday')),
		('saturday', _('Saturday')),
		('sunday', _('Sunday'))
	)

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
	routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	slug = models.SlugField(blank=True, null=True)

	day = models.CharField(max_length=30, choices=DAY_CHOICES, blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
class ExerciseRoutine(models.Model):

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
	day_routine = models.ForeignKey(DayRoutine, on_delete=models.CASCADE, blank=True, null=True)
	exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
	cycles = models.IntegerField(blank=True, null=True)
	repetitions = models.IntegerField(blank=True, null=True)
	duration = models.IntegerField(blank=True, null=True)
	rest = models.IntegerField(default=5, validators=[
		MinValueValidator(5),
	])
	slug = models.SlugField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['exercise__name']

	def __str__(self):

		day_routine = self.day_routine.name if self.day_routine else self.pk
		exercise = self.exercise.name

		return f'{day_routine} - {exercise}'
class CustomerRoutineManager(models.Manager):
	def active(self):
		return self.filter(status='active')

	def canceled(self):
		return self.filter(status='canceled')

	def completed(self):
		return self.filter(status='completed')

	def pending(self):
		return self.filter(status='pending')

	def sort_active(self):
		return self.order_by('status')
class CustomerRoutine(models.Model):
	STATUS_CHOICES = (
		('pending', 'Pendiente'),
		('active', 'Activa'),
		('completed', 'Finalizada'),
		('canceled', 'Cancelada'),
	)

	slug = models.SlugField(blank=True, null=True)
	coach = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True, related_name='coachOf')
	routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
	customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='customerOf')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = CustomerRoutineManager()

	def __str__(self):
		return f'{str(self.customer)} - {str(self.routine)}'
class CustomerRoutineProgress(models.Model):

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	customer_routine = models.ForeignKey(CustomerRoutine, on_delete=models.CASCADE)
	day = models.ForeignKey(DayRoutine, on_delete=models.CASCADE)

	current_exercise = models.ForeignKey(ExerciseRoutine, on_delete=models.CASCADE, blank=True, null=True, related_name='current_exercise')

	end_time = models.DateTimeField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.user.email

	@property
	def total_day_exercise(self):
		return self.day.exerciseroutine_set.all().count()

	@property
	def completed_exercise(self):
		return self.exerciseroutineprogress_set.all().count()

	@property
	def next_exercise(self):
		completed_exercises = self.exerciseroutineprogress_set.exclude(exercise_routine__pk = self.current_exercise.pk).values_list('exercise_routine__pk', flat=True)
		exercise_routines = self.day.exerciseroutine_set.exclude(pk__in = completed_exercises)

		prev_exercise = None
		next_exercise = None

		for i in range(0, len(exercise_routines)):
			if self.current_exercise.pk == exercise_routines[i].pk:
				if i < len(exercise_routines) - 1:
					next_exercise = exercise_routines[i+1]
			else:
				if prev_exercise is None:
					prev_exercise = exercise_routines[i]		

		if next_exercise == None and prev_exercise:
			return prev_exercise

		else:
			return next_exercise 

class ExerciseRoutineProgress(models.Model):

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	progress = models.ForeignKey(CustomerRoutineProgress, on_delete=models.CASCADE)
	exercise_routine = models.ForeignKey(ExerciseRoutine, on_delete=models.CASCADE)

	exercise_result = models.FloatField(blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.user.email} - {self.progress.pk} - {self.exercise_routine.exercise.name.capitalize()}'

@receiver(pre_save, sender=Gallery)
def pre_save_gallery(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(random_string_generator(size=16))

@receiver(pre_save, sender=Muscle)
def pre_save_muscle(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance=instance))

@receiver(pre_save, sender=Resource)
def pre_save_resource(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance=instance))

@receiver(pre_save, sender=Routine)
def pre_save_routine(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance=instance))

@receiver(pre_save, sender=Exercise)
def pre_save_exercise(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance=instance))

@receiver(pre_save, sender=Event)
def pre_save_event(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(random_string_generator(size=16))

@receiver(pre_save, sender=DayRoutine)
def pre_save_day_routine(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(random_string_generator(size=16))

@receiver(pre_save, sender=CustomerRoutine)
def pre_save_customer_routine(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(random_string_generator(size=16))

@receiver(pre_save, sender=ExerciseRoutine)
def pre_save_exercise_routine(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(random_string_generator(size=16))