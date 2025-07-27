from rest_framework import serializers
from .models import Franchise, Branch, Representative

class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = '__all__'

class FranchiseSerializer(serializers.ModelSerializer):
    owner = RepresentativeSerializer()
    franchise_image_url = serializers.SerializerMethodField()
    totalBranches = serializers.SerializerMethodField()
    branchIds = serializers.SerializerMethodField()

    class Meta:
        model = Franchise
        fields = [
            'id', 'franchise_id', 'name', 'owner', 'phone', 'business_license',
            'owner_nid', 'established_date', 'franchise_image', 'franchise_image_url',
            'overall_rating', 'status', 'created_at', 'updated_at',
            'totalBranches', 'branchIds'
        ]

    def get_franchise_image_url(self, obj):
        return obj.franchise_image.url if obj.franchise_image else None

    def get_totalBranches(self, obj):
        return obj.branches.count()

    def get_branchIds(self, obj):
        return [branch.branch_id for branch in obj.branches.all()]

    def create(self, validated_data):
        owner_data = validated_data.pop('owner')
        owner = Representative.objects.create(**owner_data)
        return Franchise.objects.create(owner=owner, **validated_data)

class BranchSerializer(serializers.ModelSerializer):
    representative = RepresentativeSerializer()
    restaurant_image_url = serializers.SerializerMethodField()
    parentFranchiseId = serializers.CharField(source='franchise.franchise_id', read_only=True)

    class Meta:
        model = Branch
        fields = [
            'id', 'branch_id', 'name', 'representative', 'phone', 'business_license',
            'owner_nid', 'established_date', 'working_period', 'large_option',
            'location', 'restaurant_image', 'restaurant_image_url', 'rating',
            'status', 'parentFranchiseId'
        ]

    def get_restaurant_image_url(self, obj):
        return obj.restaurant_image.url if obj.restaurant_image else None

    def create(self, validated_data):
        rep_data = validated_data.pop('representative', None)
        franchise = self.context['franchise']
        rep = Representative.objects.create(**rep_data) if rep_data else None
        return Branch.objects.create(representative=rep, franchise=franchise, **validated_data)
