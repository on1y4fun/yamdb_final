import django_filters
from categories.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all(),
        lookup_expr='icontains',
    )
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all(),
        lookup_expr='icontains',
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Title
        fields = (
            'genre',
            'category',
            'name',
            'year',
        )
