from django import template
from django.db.models import Q
from apps.training.models import ExerciseRoutineProgress, CustomerRoutine, Muscle, Resource
register = template.Library()


@register.inclusion_tag('training/custom_tags/is_completed.html')
def check_is_completed(**kwargs):
    exercise_routine = kwargs.get('exercise_routine')
    progress = kwargs.get('progress')

    qs = ExerciseRoutineProgress.objects.filter(
        exercise_routine__pk=exercise_routine, progress__pk=progress)
    return {'result': qs.exists()}


@register.inclusion_tag('training/custom_tags/muscle_filter.html')
def muscles_filter(**kwargs):
    qs = kwargs.get('qs')

    muscles = Muscle.objects.filter(exercise__in=qs).order_by().distinct()
    print(muscles)

    return {'result': muscles}

@register.inclusion_tag('training/custom_tags/resource_filter.html')
def resource_filter(**kwargs):
    qs = kwargs.get('qs')

    resources = Resource.objects.filter(exercise__in=qs).order_by().distinct()
    print(resources)

    return {'result': resources}

@register.inclusion_tag('training/custom_tags/title_filter.html')
def title_filter(**kwargs):
    muscle = kwargs.get('muscle', None)
    resource = kwargs.get('resource', None)

    return {'muscle': muscle, 'resource': resource}


@register.simple_tag
def is_completed(**kwargs):

    exercise_routine = kwargs.get('exercise_routine')
    progress = kwargs.get('progress')
    qs = ExerciseRoutineProgress.objects.filter(
        exercise_routine=exercise_routine, progress=progress)
    return qs.exists()


@register.simple_tag
def is_active_customer(**kwargs):

    customer = kwargs.get('customer')
    coach = kwargs.get('coach')

    qs = CustomerRoutine.objects.filter(
        customer=customer, coach=coach, status='active')

    return qs.exists()


@register.simple_tag
def active_routine(**kwargs):

    customer = kwargs.get('customer')
    try:
        qs = CustomerRoutine.objects.get(customer=customer, status='active')
        return qs
    except CustomerRoutine.DoesNotExist:
        return False
