from django.core.exceptions import PermissionDenied

class UserIsCoachMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.user_type == 'coach':
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class CustomerHasTrainingMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.user_type == 'customer' and self.request.user.enable_training:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied