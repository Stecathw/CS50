from django.conf import settings
from .models import Category

def category_dropdown(request):
    """
    Created this context processor in order to populate dropdown list in the layout template,
    -> bootstrap dropdown navbar.
    """
    return {'categories': Category.objects.all().order_by('name')}