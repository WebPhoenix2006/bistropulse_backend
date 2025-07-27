from rest_framework import serializers
from .models import Franchise, Branch, Representative


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = "__all__"


class FranchiseSerializer(serializers.ModelSerializer):
    owner = RepresentativeSerializer()

    class Meta:
        model = Franchise
        fields = "__all__"

    def create(self, validated_data):
        owner_data = validated_data.pop("owner")
        owner = Representative.objects.create(**owner_data)
        franchise = Franchise.objects.create(owner=owner, **validated_data)
        return franchise

    def update(self, instance, validated_data):
        owner_data = validated_data.pop("owner", None)
        if owner_data:
            for attr, value in owner_data.items():
                setattr(instance.owner, attr, value)
            instance.owner.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BranchSerializer(serializers.ModelSerializer):
    representative = RepresentativeSerializer()

    class Meta:
        model = Branch
        fields = "__all__"

    def create(self, validated_data):
        rep_data = validated_data.pop("representative")
        rep = Representative.objects.create(**rep_data)
        branch = Branch.objects.create(representative=rep, **validated_data)
        return branch

    def update(self, instance, validated_data):
        rep_data = validated_data.pop("representative", None)
        if rep_data:
            for attr, value in rep_data.items():
                setattr(instance.representative, attr, value)
            instance.representative.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
