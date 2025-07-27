from rest_framework import serializers
from .models import Franchise, Branch, Representative


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = "__all__"


class FranchiseSerializer(serializers.ModelSerializer):
    owner = RepresentativeSerializer()
    franchise_id = serializers.CharField(read_only=True)

    class Meta:
        model = Franchise
        fields = "__all__"
        read_only_fields = ["franchise_id", "created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        owner_data = validated_data.pop("owner")
        owner = Representative.objects.create(**owner_data)
        user = self.context["request"].user
        return Franchise.objects.create(owner=owner, created_by=user, **validated_data)

    def update(self, instance, validated_data):
        owner_data = validated_data.pop("owner", None)
        if owner_data:
            rep = instance.owner
            for attr, value in owner_data.items():
                setattr(rep, attr, value)
            rep.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BranchSerializer(serializers.ModelSerializer):
    representative = RepresentativeSerializer()
    branch_id = serializers.CharField(read_only=True)

    class Meta:
        model = Branch
        fields = "__all__"
        read_only_fields = ["franchise", "branch_id", "created_by"]

    def create(self, validated_data):
        rep_data = validated_data.pop("representative")
        rep = Representative.objects.create(**rep_data)
        user = self.context["request"].user
        return Branch.objects.create(representative=rep, created_by=user, **validated_data)

    def update(self, instance, validated_data):
        rep_data = validated_data.pop("representative", None)
        if rep_data:
            rep = instance.representative
            for attr, value in rep_data.items():
                setattr(rep, attr, value)
            rep.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
