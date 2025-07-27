from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from .models import Franchise, Branch, Representative
from .serializers import FranchiseSerializer, BranchSerializer


class FranchiseListCreateView(generics.ListCreateAPIView):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        rep_data = self.request.data.get("representative")
        if not rep_data:
            raise ValidationError({"representative": ["This field is required."]})
        serializer.is_valid(raise_exception=True)
        serializer.save()


class BranchListCreateView(generics.ListCreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        franchise_id = self.kwargs["franchise_id"]
        return Branch.objects.filter(franchise__id=franchise_id)

    def perform_create(self, serializer):
        franchise_id = self.kwargs["franchise_id"]
        try:
            franchise = Franchise.objects.get(id=franchise_id)
        except Franchise.DoesNotExist:
            raise ValidationError({"franchise": ["Invalid franchise ID."]})

        serializer.is_valid(raise_exception=True)
        serializer.save(franchise=franchise)
