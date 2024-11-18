from .models import Category


def navlist(request):
    return {
        'categories': Category.objects.filter(is_active=True),
    }
