from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
	ExerciseRoutineProgressSerializer, CustomerRoutineProgressSerializer, CoachCustomerRoutineSerializer)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsCoach, IsCustomer
from apps.training.models import (
	CustomerRoutine, Routine, Exercise, ExerciseRoutineProgress, CustomerRoutineProgress)

from apps.training.services import CustomerRoutineProgressService

class ExerciseRoutineProgressViewSet(viewsets.ModelViewSet):
	serializer_class = ExerciseRoutineProgressSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return ExerciseRoutineProgress.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class CustomerRoutineProgressListView(generics.ListAPIView):
	serializer_class = CustomerRoutineProgressSerializer
	permission_classes = [IsAuthenticated, IsCustomer]

	def get_queryset(self):
		today = timezone.now().today()
		start_of_week, end_of_week = CustomerRoutineProgressService.get_start_and_end_date(today, date_range='week')

		active_customer_routine =  self.request.user.customerOf.active()
		return CustomerRoutineProgress.objects.filter(user=self.request.user,
														customer_routine=active_customer_routine.first(),
														created_at__date__range=[start_of_week, end_of_week],
													)


class CoachCustomerRoutineListView(generics.ListAPIView):
	serializer_class = CoachCustomerRoutineSerializer
	permission_classes = [IsAuthenticated, IsCoach]

	def get_serializer_context(self):
		context = super().get_serializer_context()

		today = timezone.now().today()
		start_of_week, end_of_week = CustomerRoutineProgressService.get_start_and_end_date(today, date_range='week')

		context['date_range'] = (start_of_week, end_of_week)
		return context

	def get_queryset(self):
		today = timezone.now().today()
		return CustomerRoutine.objects.filter(coach=self.request.user, status='active',)
