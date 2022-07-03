from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, views, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Budget, Record
from users.models import User
from .serializers import BudgetSerializer, RecordSerializer
from .paginations import BudgetsPagination
from family_budget.permissions import IsOwnerOrAdmin


class BudgetViewSet(viewsets.ModelViewSet):

    serializer_class = BudgetSerializer
    pagination_class = BudgetsPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['balance', 'date_created']

    def get_queryset(self):
        queryset = Budget.objects.all()
        min_date = self.request.query_params.get('min_date')
        max_date = self.request.query_params.get('max_date')
        if any((min_date, max_date)):
            queryset = queryset.filter(date_created__range=(min_date, max_date))
        return queryset

    def get_permissions(self):
        if self.action in ["create", "list"]:
            return (IsAuthenticated(),)
        if self.action in ["destroy", "update", "partial_update"]:
            return (
                IsOwnerOrAdmin(),
            )
        else:
            return (AllowAny(),)

    def list(self, request):
        queryset = self.get_queryset()
        if not request.user.is_staff and queryset:
            queryset = queryset.filter(owner=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        budget_serializer = self.serializer_class(data=data)
        if budget_serializer.is_valid():
            budget_serializer.save(owner=request.user)
            return Response(budget_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(budget_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareBudget(generics.ListCreateAPIView):

    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsOwnerOrAdmin, ]

    def patch(self, request, format=None):
        data = request.data
        budget = get_object_or_404(Budget, pk=data["budget"])
        if budget.owner != request.user:
            return Response("Cannot share other users' budgets", status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=data["user"])
        if user == budget.owner:
            return Response("Cannot share with yourself", status=status.HTTP_403_FORBIDDEN)

        budget.shared_with.add(user)
        return Response(f"Budget shared with user {user.username}", status=status.HTTP_200_OK)


class UnShareBudget(generics.ListCreateAPIView):

    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsOwnerOrAdmin, ]

    def patch(self, request, format=None):
        data = request.data
        budget = get_object_or_404(Budget, pk=data["budget"])
        if request.user not in [*budget.shared_with.all(), budget.owner]:
            return Response("Cannot unshare others from other users' budgets", status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=data["user"])
        if user == budget.owner:
            return Response("Cannot unshare with yourself", status=status.HTTP_403_FORBIDDEN)

        budget.shared_with.remove(user)
        return Response(f"Budget shared with user {user.username}", status=status.HTTP_200_OK)


class SharedWithMe(generics.ListAPIView):

    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classess = [IsAuthenticated, ]

    def get(self, request):
        queryset = self.queryset.filter(shared_with__username=request.user.username)
        return Response(BudgetSerializer(queryset, many=True).data)


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_permissions(self):
        if self.action == "create":
            return (IsAuthenticated(),)
        if self.action in ["update", "partial_update", "details_view"]:
            return (
                IsAuthenticated(),
                IsOwnerOrAdmin(),
            )
        else:
            return (AllowAny(),)

    def list(self, request):
        return Response("Cannot list incomes/expenses outside budgets", status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        data = request.data
        record_serializer = self.serializer_class(data=data)
        if record_serializer.is_valid():
            budget = Budget.objects.get(pk=data["budget"])
            if not request.user == budget.owner:
                return Response("You cant only add record the the budgets you own", status=status.HTTP_403_FORBIDDEN)
            record_serializer.save(budget=budget)
            return Response(record_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(record_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        record = get_object_or_404(Record, pk=pk)
        budget = record.budget
        if request.user == budget.owner or request.user.is_staff:
            record.delete()
            return Response(f"Record {pk} deleted", status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
