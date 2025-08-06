from rest_framework import serializers
from customers.models import Customer
from franchise.models import Branch
from orders.models import Order
from restaurants.models import Rider
from restaurants.serializers import RiderSerializer
from customers.serializers import CustomerSerializer
from django.contrib.gis.geos import Point


class PointField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Point):
            return {"lat": value.y, "lng": value.x}
        return value

    def to_internal_value(self, data):
        try:
            lat = float(data.get("lat"))
            lng = float(data.get("lng"))
            return Point(lng, lat)
        except (TypeError, ValueError):
            raise serializers.ValidationError("Invalid coordinates format.")


class OrderSerializer(serializers.ModelSerializer):
    rider = RiderSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

    rider_id = serializers.PrimaryKeyRelatedField(
        queryset=Rider.objects.all(), write_only=True, required=False
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), write_only=True
    )
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), write_only=True, required=False
    )

    pickup_location = PointField(required=False)
    dropoff_location = PointField(required=False)
    current_location = PointField(required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "rider", "rider_id",
            "customer", "customer_id",
            "branch", "branch_id",
            "pickup_location",
            "dropoff_location",
            "current_location",
            "status",
            "date_ordered",
            "date_delivered",
            "payment_method",
            "payment_status",
            "delivery_fee",
            "platform_fee",
            "tax",
            "total",
        ]
        read_only_fields = ["id", "total", "rider", "customer", "branch"]

    def create(self, validated_data):
        rider = validated_data.pop("rider_id", None)
        customer = validated_data.pop("customer_id")
        branch = validated_data.pop("branch_id", None)

        order = Order.objects.create(
            rider=rider,
            customer=customer,
            branch=branch,
            **validated_data
        )
        return order
