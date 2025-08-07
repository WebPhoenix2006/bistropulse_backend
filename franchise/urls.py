from django.urls import path
from .views import (
    FranchiseListCreateView,
    FranchiseRetrieveUpdateDestroyView,
    BranchListCreateView,
    BranchRetrieveUpdateDestroyView
)

urlpatterns = [
    # Franchise endpoints
    path("", FranchiseListCreateView.as_view(), name="franchise-list-create"),
    path("<str:franchise_id>/", FranchiseRetrieveUpdateDestroyView.as_view(), name="franchise-detail"),

    # Branch endpoints under a franchise
    path("<str:franchise_id>/branches/", BranchListCreateView.as_view(), name="branch-list-create"),
    path("<str:franchise_id>/branches/<str:branch_id>/", BranchRetrieveUpdateDestroyView.as_view(), name="branch-detail"),
]
