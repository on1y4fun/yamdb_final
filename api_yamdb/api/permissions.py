from rest_framework import permissions


class OnlyAdminAndSuperuser(permissions.BasePermission):
    """Определяет права на изменения только для Суперпользователя
    или Админа.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Определяет права на изменения для админа и аутентифицированного
    пользователя или юзера со статусом ReadOnly.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_admin
        )


class IsAdminModeratorOrReadOnly(permissions.BasePermission):
    """Определяет права на изменения для админа, модератора и автора
    отзывов и комментариев.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAdminSuperuserOrReadOnly(permissions.BasePermission):
    """Определяет права на получение данных для всех и права на изменения
    только для Суперпользователя или Админа.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_superuser or request.user.is_admin)
        )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
