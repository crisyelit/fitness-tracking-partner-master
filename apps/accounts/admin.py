from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,
					 )


# Register your models here.
class CustomUserAdmin(UserAdmin):
	list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'public_id', 'user_type', 'parent')
	fieldsets = UserAdmin.fieldsets + (
		('Extra Fields', {
			'fields': (
				'parent',
				'phone',
				'user_type',
				'address',
				'zip_code',
				'image',
				'public_id',
				'enable_training',
				'enable_nutrition',
				'enable_tracking',
				'is_email_confirmed',
				'is_whatsapp',
			),
		}),
	)


admin.site.register(User, CustomUserAdmin)
