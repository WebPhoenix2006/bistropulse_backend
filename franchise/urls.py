from django.urls import path
from .views import FranchiseListCreateView, BranchListCreateView

urlpatterns = [
    path('', FranchiseListCreateView.as_view(), name='franchise-list-create'),
    path('<int:franchise_id>/branches/', BranchListCreateView.as_view(), name='branch-list-create'),
]
