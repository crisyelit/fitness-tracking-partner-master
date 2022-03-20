from django.contrib import admin

from .models import (
    Gallery,
    Tag,
    Routine,
    Muscle,
    Resource,
    Exercise,
    ExerciseRoutine,
    CustomerRoutine,
    CustomerRoutineProgress,
    ExerciseRoutineProgress,
    DayRoutine,
    Event,
)

# Register your models here.
admin.site.register(Event)
admin.site.register(Muscle)
admin.site.register(Gallery)
admin.site.register(Tag)
admin.site.register(Resource)
admin.site.register(Routine)
admin.site.register(Exercise)

class DayRoutineAdmin(admin.ModelAdmin):
    list_display = ("name", "routine", "day")
admin.site.register(DayRoutine, DayRoutineAdmin)
class ExerciseRoutineAdmin(admin.ModelAdmin):
    list_display = ("day_routine", "exercise")

admin.site.register(ExerciseRoutine, ExerciseRoutineAdmin)


class CustomerRoutineAdmin(admin.ModelAdmin):
    list_display = ("routine", "customer", "coach", "status", "start_date", "end_date")

admin.site.register(CustomerRoutine, CustomerRoutineAdmin)
class CustomerRoutineAdmin(admin.ModelAdmin):
    list_display = ("user", "customer_routine", "day", "current_exercise", "completed_exercise", 'total_day_exercise', "created_at", "end_time")

admin.site.register(CustomerRoutineProgress, CustomerRoutineAdmin)

class ExerciseRoutineProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "progress", "exercise_routine", "exercise_result")

admin.site.register(ExerciseRoutineProgress, ExerciseRoutineProgressAdmin)

