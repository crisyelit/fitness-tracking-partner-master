import datetime
from django.utils import timezone
from django.db.models import Count, Q
from .models import CustomerRoutineProgress, CustomerRoutine, ExerciseRoutine, ExerciseRoutineProgress

# FALTA VALIDAR LOS DIAS


class CustomerRoutineProgressService:
	first_model = CustomerRoutine
	second_model = CustomerRoutineProgress

	def __init__(self, user, *args, **kwargs):
		self.user = user
		self.customer_routine = None
		self.day_routines = None
		self.day_routine_progress = None

		self.today = timezone.now()

	@classmethod
	def get_start_and_end_date(cls, date, **kwargs):
		start_of_week = date.date() - datetime.timedelta(days=date.weekday())  # Monday
		end_of_week = start_of_week + datetime.timedelta(days=6)  # Sunday

		return (start_of_week, end_of_week)
				 
	def validate_customer_routine(self):

		self.customer_routine = self.user.customerOf.filter(status='active')
		if not self.customer_routine.exists():
			return {'code': 'CUSTOMER_ROUTINE_DOES_NOT_EXIST', 'message': 'No tienes una rutina activa'}

		self.customer_routine = self.customer_routine.first()

		if self.customer_routine.start_date and self.customer_routine.end_date:
			if self.today.date() < self.customer_routine.start_date or self.today.date() > self.customer_routine.end_date:
				return {
					"code": "CUSTOMER_ROUTINE_EXPIRED",
					"message": "La rutina del cliente ha expirado"
				}

		return {
			"code": "VALID",
			"message": "Rutina válida"
		}

	def get_or_create_day_routine(self):
		start_of_week, end_of_week = self.get_start_and_end_date(self.today)

		self.day_routines = self.customer_routine.routine.dayroutine_set.all()
		response = {
			"code": "EMPTY_DAY_ROUTINE",
			"message": "No tienes ejercicios disponibles. Toma un descanso"
		}

		for day in self.day_routines:
			print('start_of_week', start_of_week)
			print('end_of_week', end_of_week)
			print(self.user, self.customer_routine, day)

			if day.day and day.day.lower() != self.today.strftime("%A").lower():
				continue

			day_routine_progress_qs = self.second_model.objects.filter(
				user=self.user,
				customer_routine=self.customer_routine,
				day=day,
				created_at__date__range=[start_of_week, end_of_week],
			)

			print(day_routine_progress_qs)
			if day_routine_progress_qs.exists() != True:
				print('not exist')
				self.day_routine_progress = self.second_model.objects.create(
					user=self.user,
					customer_routine=self.customer_routine,
					day=day,
					current_exercise=day.exerciseroutine_set.first(),
				)

				print(self.day_routine_progress.created_at.date())
				response = {
					"code": "CREATED",
					"progress": self.day_routine_progress
				}
				break

			if day_routine_progress_qs.first().created_at.date() == self.today.date():
				self.day_routine_progress = day_routine_progress_qs.first()

				response = {
					"code": "GET",
					"progress": self.day_routine_progress
				}
				break


		return response

	def set_current_exercise(self, exercise):
		try:
			exercise = self.day_routine_progress.day.exerciseroutine_set.get(slug=exercise)
			self.day_routine_progress.current_exercise = exercise
			self.day_routine_progress.save()

			return {
				'code': 'SAVED',
				'current_exercise':  self.day_routine_progress.current_exercise
			}
		except ExerciseRoutine.DoesNotExist:
			return {
				'code': 'INVALID_EXERCISE_ROUTINE',
				'message': 'Exercise Routine invalid'
			}

	def get_day_progress(self):
		
		if self.day_routine_progress.completed_exercise < self.day_routine_progress.total_day_exercise:
			return {
				"code": "IN_PROGRESS",
				"completed_exercise": self.day_routine_progress.completed_exercise,
				"total_day_exercise": self.day_routine_progress.total_day_exercise
			}


		if self.day_routine_progress.end_time == None:
			self.day_routine_progress.end_time = self.today
			self.day_routine_progress.save()
			
		return {
			"code": "COMPLETED",
			"message": "¡Hemos terminado la rutina de hoy! toma un descanso"
		}



