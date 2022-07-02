from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Basic CRUD for a User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            return IsAuthenticated()
        return (AllowAny(),)
