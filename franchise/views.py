from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Franchise, Branch
from .serializers import FranchiseSerializer, BranchSerializer


class FranchiseListCreateView(generics.ListCreateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [IsAuthenticated]


class BranchListCreateView(generics.ListCreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        franchise_id = self.kwargs["franchise_id"]
        return Branch.objects.filter(franchise__franchise_id=franchise_id)

    def perform_create(self, serializer):
        franchise_id = self.kwargs["franchise_id"]
        franchise = Franchise.objects.get(franchise_id=franchise_id)
        serializer.save(franchise=franchise)
