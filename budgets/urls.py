from django.urls import path, include
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"budgets", views.BudgetViewSet, basename="budgets")
router.register(r"records", views.RecordViewSet, basename="records")

urlpatterns = [
    path("", include(router.urls)),
    path("share/", views.ShareBudget.as_view(), name="share_budget"),
    path("unshare/", views.UnShareBudget.as_view(), name="unshare_budget"),
    path("shared/", views.SharedWithMe.as_view(), name="shared"),
]
