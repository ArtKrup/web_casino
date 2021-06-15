from django.db.models import Count
from django.core.cache import cache

from .models import Category

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Главная страница', 'url_name': 'home'},
        {'title': 'Обратная связь', 'url_name': 'feedback'},
        {'title': 'Добавление статьи', 'url_name': 'addpage'}]


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.annotate(Count('games'))
            cache.set('categories', categories, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(-1)
        context['menu'] = user_menu
        context['categories'] = categories
        return context



