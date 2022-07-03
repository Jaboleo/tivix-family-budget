from django.urls import path, include
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"budgets", views.BudgetViewSet)
router.register(r"records", views.RecordViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("share/", views.ShareBudget.as_view(), name="share_budget"),
    path("unshare/", views.UnShareBudget.as_view(), name="unshare_budget"),
    path("shared-with-me/", views.SharedWithMe.as_view(), name="shared_with_me"),
]
