from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from family_budget.permissions import IsThisUserOrAdmin
from .models import User
from .serializers import UserSerializer
from .paginations import UsersPagination


class UserViewSet(ModelViewSet):
    """Basic CRUD for a User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UsersPagination

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            return (IsThisUserOrAdmin(),)
        return (AllowAny(),)

    # pylint: disable=arguments-differ
    def destroy(self, request, pk=None):
        user_to_delete = User.objects.get(pk=pk)
        self.check_object_permissions(self.request, user_to_delete)
        user_to_delete.delete()
        return Response(f"User with id {pk} successfully deleted!")
