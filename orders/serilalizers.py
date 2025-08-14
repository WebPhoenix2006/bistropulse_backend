from rest_framework import serializers
from customers.models import Customer
from franchise.models import Branch
from orders.models import Order, Item
from restaurants.models import Rider, Restaurant
from restaurants.serializers import RiderSerializer
from customers.serializers import CustomerSerializer
from django.contrib.gis.geos import Point


class StringLookupRelatedField(serializers.RelatedField):
    """
    Allows related lookup by a unique string field (like 'customer_id' or 'rider_code').
    """

    def __init__(self, queryset, lookup_field, **kwargs):
        self.lookup_field = lookup_field
        super().__init__(queryset=queryset, **kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.lookup_field: data})
        except self.get_queryset().model.DoesNotExist:
            raise serializers.ValidationError(
                f"{self.lookup_field} '{data}' does not exist."
            )

    def to_representation(self, value):
        return getattr(value, self.lookup_field)


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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["food", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(read_only=True)

    rider = RiderSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

    rider_code = StringLookupRelatedField(
        queryset=Rider.objects.all(),
        lookup_field="rider_code",
        write_only=True,
        required=False,
    )
    customer_code = StringLookupRelatedField(
        queryset=Customer.objects.all(), lookup_field="customer_id", write_only=True
    )
    branch_code = StringLookupRelatedField(
        queryset=Branch.objects.all(),
        lookup_field="branch_id",
        write_only=True,
        required=False,
    )
    restaurant_code = StringLookupRelatedField(
        queryset=Restaurant.objects.all(),
        lookup_field="restaurant_id",  # or change to your actual code field
        write_only=True,
        required=False,
    )

    pickup_location = PointField(required=False)
    dropoff_location = PointField(required=False)
    current_location = PointField(required=False)

    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            "order_id",
            "rider",
            "rider_code",
            "customer",
            "customer_code",
            "restaurant",
            "restaurant_code",
            "branch",
            "branch_code",
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
            "items",
        ]
        read_only_fields = ["total", "rider", "customer", "branch", "restaurant"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        rider = validated_data.pop("rider_code", None)
        customer = validated_data.pop("customer_code")
        branch = validated_data.pop("branch_code", None)
        restaurant = validated_data.pop("restaurant_code", None)

        # Fallback: restaurant from context
        if not branch and not restaurant:
            restaurant_id = self.context.get("restaurant_id")
            if restaurant_id:
                try:
                    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
                except Restaurant.DoesNotExist:
                    raise serializers.ValidationError(
                        {
                            "restaurant_id": f"Restaurant with id '{restaurant_id}' does not exist."
                        }
                    )

        order = Order.objects.create(
            rider=rider,
            customer=customer,
            branch=branch,
            restaurant=restaurant,
            **validated_data,
        )

        # Create order items
        for item in items_data:
            Item.objects.create(order=order, **item)

        return order
