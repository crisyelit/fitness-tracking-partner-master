from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.training.models import (ExerciseRoutineProgress,
                                  Muscle,
                                  Exercise,
                                  Routine,
                                  DayRoutine,
                                  ExerciseRoutine,
                                  CustomerRoutine,
                                  CustomerRoutineProgress)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'public_id', 'get_full_name')
class MuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muscle
        fields = (
            'name',
        )

        read_only_fields = ['id',  'slug']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = (
            'name',
            'warnings',
            'resources',
            'description',
            'muscles',
            'gallery',
            'status',
            'is_default',
            'image',
            'video',
        )

        read_only_fields = ['id', 'created_at', 'updated_at', 'slug']


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = (
            'name',
            'description',
        )

        read_only_fields = ['id', 'created_at', 'updated_at', 'slug']

    

class DayRoutineSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    routine = RoutineSerializer()
    class Meta:
        model = DayRoutine
        fields = (
            'routine',
            'name',
            'day',
        )

        read_only_fields = ['id', 'created_at', 'updated_at', 'slug']

    def get_name(self, obj):
        return obj.name.capitalize() if obj.name else ''

    def get_day(self, obj):
        return obj.day.capitalize() if obj.day else ''


class ExerciseRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRoutine
        fields = (
            'exercise',
            'cycles',
            'repetitions',
            'duration',
            'rest',
        )

        read_only_fields = ['id', 'created_at', 'updated_at', 'slug']


class CustomerRoutineSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer()
    routine_total_day = serializers.SerializerMethodField()
    class Meta:
        model = CustomerRoutine
        fields = (
            'coach',
            'routine',
            'status',
            'start_date',
            'end_date',
            'routine_total_day',
        )

        read_only_fields = ['id', 'created_at', 'updated_at', 'slug', 'routine_total_day']

    def get_routine_total_day(self, obj):
        return obj.routine.dayroutine_set.count()

class CustomerRoutineProgressSerializer(serializers.ModelSerializer):
    customer_routine = CustomerRoutineSerializer()
    day = DayRoutineSerializer()
    current_exercise = ExerciseRoutineSerializer()
    total_day_exercise = serializers.SerializerMethodField()
    completed_exercise = serializers.SerializerMethodField()
    created_at_date = serializers.SerializerMethodField()
    class Meta:
        model = CustomerRoutineProgress
        fields = (
            'id',
            'customer_routine',
            'day',
            'current_exercise',
            'end_time',
            'total_day_exercise',
            'completed_exercise',
            'created_at',
            'updated_at',
            'created_at_date',
        )

        read_only_fields = ['id', 
                            'total_day_exercise',
                            'completed_exercise',
                            'created_at',
                            'created_at_date',
                            'updated_at']

    def get_total_day_exercise(self, obj):
        return obj.total_day_exercise

    def get_completed_exercise(self, obj):
        return obj.completed_exercise

    def get_created_at_date(self, obj):
        return obj.created_at.strftime('%d/%m/%Y')

class ExerciseRoutineProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseRoutineProgress
        fields = (
            'id',
            'progress',
            'exercise_routine',
            'exercise_result', 
            'created_at',
            'updated_at',
            )

        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Check that start is before finish.
        """

        progress = data['progress']
        exercise_routine = data['exercise_routine']

        qs = ExerciseRoutineProgress.objects.filter(exercise_routine=exercise_routine, progress=progress)
        print(qs)
        if qs.exists():
            raise serializers.ValidationError("Exercise routine exist in progress")

        return data


class CoachCustomerRoutineSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer()
    customer = CustomerSerializer()
    routine_total_day = serializers.SerializerMethodField()
    routine_total_day_completed = serializers.SerializerMethodField()
    routine_total_day_progress = serializers.SerializerMethodField()
    class Meta:
        model = CustomerRoutine
        fields = (
            'customer',
            'routine',
            'status',
            'start_date',
            'end_date',
            'routine_total_day',
            'routine_total_day_completed',
            'routine_total_day_progress',
        )

        read_only_fields = ['id', 'created_at', 'updated_at', 'slug', 'routine_total_day']

    def get_routine_total_day(self, obj):
        return obj.routine.dayroutine_set.count()

    def get_routine_total_day_completed(self, obj):
        date_range = self.context.get('date_range', False)

        if date_range:
            return obj.customerroutineprogress_set.filter(
                created_at__date__range=[date_range[0], date_range[1]],
            ).count()

        return 0

    def get_routine_total_day_progress(self, obj):
        date_range = self.context.get('date_range', False)

        if date_range:
            progress =  obj.customerroutineprogress_set.filter(
                created_at__date__range=[date_range[0], date_range[1]],
            ).count()
            total_day = obj.routine.dayroutine_set.count()

            return progress * 100 / total_day


        return 0