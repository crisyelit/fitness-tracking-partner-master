from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Exercise, Muscle, Resource, Routine, CustomerRoutineProgress, CustomerRoutine, DayRoutine

User = get_user_model()

@registry.register_document
class ExerciseDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'public_id': fields.TextField(),
    })

    class Index:
        name = 'exercises'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Exercise

        fields = [
            'name',
            'slug',
            'warnings',
            'description',
            'level',
            'created_at',
        ]

    def get_queryset(self):
        return super(ExerciseDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.exercises.all()

class CustomerRoutineProgressDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'public_id': fields.TextField(),
    })

    customer_routine = fields.ObjectField(properties={
        'id': fields.IntegerField(),
    })

    day = fields.ObjectField(properties={
        'id': fields.IntegerField(),
    })

    class Index:
        name = 'customerroutineprogress'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = CustomerRoutineProgress

        fields = [
            'created_at',
        ]

    def get_queryset(self):
        return super(ExerciseDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.customerroutineprogress.all()
        elif isinstance(related_instance, CustomerRoutine):
            return related_instance.customerroutineprogress.all()
        elif isinstance(related_instance, DayRoutine):
            return related_instance.customerroutineprogress.all()