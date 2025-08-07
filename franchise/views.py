from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Franchise, Branch
from .serializers import FranchiseSerializer, BranchSerializer


class FranchiseListCreateView(generics.ListCreateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save()


class FranchiseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "franchise_id"
    parser_classes = [MultiPartParser, FormParser]


class BranchListCreateView(generics.ListCreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        franchise_id = self.kwargs.get("franchise_id")
        return Branch.objects.filter(franchise__franchise_id=franchise_id)

    def perform_create(self, serializer):
        franchise_id = self.kwargs.get("franchise_id")
        franchise = get_object_or_404(Franchise, franchise_id=franchise_id)
        serializer.save(franchise=franchise)


class BranchRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "branch_id"

    def get_queryset(self):
        franchise_id = self.kwargs.get("franchise_id")
        return Branch.objects.filter(franchise__franchise_id=franchise_id)
