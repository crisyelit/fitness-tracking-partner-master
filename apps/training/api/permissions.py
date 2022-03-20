from rest_framework import permissions

class IsCoach(permissions.BasePermission):
	"""
	Global permission check for blocked IPs.
	"""

	def has_permission(self, request, view):
		return request.user.user_type == 'coach'

class IsCustomer(permissions.BasePermission):
	"""
	Global permission check for blocked IPs.
	"""

	def has_permission(self, request, view):
		return request.user.user_type == 'customer'
