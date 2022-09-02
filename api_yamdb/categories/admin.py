from django.contrib import admin

from categories.models import Genre, Category, Title, TitleGenre


class GenreInline(admin.TabularInline):
    model = TitleGenre


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    inlines = (GenreInline,)


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
