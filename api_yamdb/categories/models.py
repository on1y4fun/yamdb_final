from django.db import models


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг-название жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг-название категории',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год',
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория произведения',
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        verbose_name='Произведение',
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр произведения',
        null=True,
    )

    def __str__(self):
        return f'{self.genre} {self.title}'
