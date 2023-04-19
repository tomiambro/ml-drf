from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import CreateUserSerializer, UserSerializer

User = get_user_model()


class UserViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # Register a new user
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = CreateUserSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            # serializer.save()
            User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data.get("email", ""),
                password=serializer.validated_data["password"],
            )
            return Response(
                status=status.HTTP_201_CREATED, data=serializer.validated_data
            )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
