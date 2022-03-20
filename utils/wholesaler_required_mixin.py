from django.contrib.auth.decorators import login_required
from django.http import Http404


class WholeSalerRequiredMixin(object):
	"""
	View mixin which requires that the authenticated user is a super user
	(i.e. `is_superuser` is True).
	"""

	@login_required
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_superuser or not request.user.is_staff or not request.user.profile.is_wholesaler:
			raise Http404
		return super(WholeSalerRequiredMixin, self).dispatch(request,*args, **kwargs)