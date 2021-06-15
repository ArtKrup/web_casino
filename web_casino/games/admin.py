from django.contrib import admin
from .models import Games, Category


class GamesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create', 'time_update', 'image')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'rules', 'payouts')
    list_filter = ('time_create', 'cat')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'cat', 'rules', 'image', 'payouts')
    readonly_fields = ('time_create', 'time_update')
    save_on_top = True

    # def get_html_image(self, object):
    #     if object.image:
    #         return mark_safe(f"<img src='{object.image.url}' width=50>")

    # get_html_image.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Games, GamesAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = "Админ-панель Casino Assistant"
admin.site.site_header = "Админ-панель Casino Assistant"
