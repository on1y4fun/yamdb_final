from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import User
from api.permissions import OnlyAdminAndSuperuser
from api.serializers import (
    AdminUserSerializer,
    GetTokenSerializer,
    RegisterSerializer,
    UserSerializer,
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer = GetTokenSerializer(data=serializer.data)

    if serializer.is_valid():
        data = {'token': serializer.data.get('token')}
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (permissions.IsAuthenticated, OnlyAdminAndSuperuser)
    pagination_class = PageNumberPagination

    @action(
        methods=('get', 'patch', 'delete',),
        url_path=r'(?P<username>\w+)',
        detail=False,
    )
    def admin_functions(self, request, username):
        user = get_object_or_404(User, username=username)

        if request.method == 'GET':
            serializer = AdminUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            data = request.data.copy()
            data['username'] = user.username
            data['email'] = user.email
            serializer = AdminUserSerializer(user, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):
    @staticmethod
    def get(request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
