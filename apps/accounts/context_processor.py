from django.contrib.auth import get_user_model

def leaders_renderer(request):
    return {
       "featured_leaders": get_user_model().objects.all()[:5],
    }