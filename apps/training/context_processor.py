from .models import Category


def categories_renderer(request):
    return {
       "all_categories": Category.objects.all(),
    }