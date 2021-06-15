from django import template
from ..models import *

register = template.Library()


@register.simple_tag(name='get_all_categories')
def get_all_categories():
    return Category.objects.all()


@register.inclusion_tag('games/list_categories.html')
def show_all_categories():
    categories = Category.objects.all()
    return {'categories': categories}
