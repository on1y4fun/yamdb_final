from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, viewsets

from api.permissions import (
    IsAdminSuperuserOrReadOnly,
    OnlyAdminAndSuperuser,
    ReadOnly,
)
from categories.models import Category, Genre, Title
from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)


class CategoryGenreViewSet(viewsets.ModelViewSet):
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
            return obj
        except ObjectDoesNotExist:
            raise exceptions.MethodNotAllowed(method='GET')

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return (ReadOnly(),)
        if self.request.method == 'POST':
            return (OnlyAdminAndSuperuser(),)
        return super().get_permissions()


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return (ReadOnly(),)
        if self.request.method == 'POST':
            return (OnlyAdminAndSuperuser(),)
        return super().get_permissions()

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score')).order_by(
            'name'
        )
