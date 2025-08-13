from django.contrib.gis.db import models as gis_models
from django.db import models
import random
from django.contrib.auth import get_user_model
from django.conf import settings
from django.forms import ValidationError
from restaurants.models import Food, Restaurant, Rider
from franchise.models import Branch
from customers.models import Customer

User = get_user_model()


def generate_unique_id():
    while True:
        new_id = f"BO{random.randint(1000000, 9999999)}"
        if not Order.objects.filter(id=new_id).exists():
            return new_id


class Order(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=10,
        unique=True,
        editable=False,
        default=generate_unique_id,
    )
    rider = models.ForeignKey(
        Rider, on_delete=models.CASCADE, null=True, blank=True, related_name="orders"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="orders"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="orders",
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True, related_name="orders"
    )

    # GIS Fields for pickup/dropoff and current rider location
    pickup_location = gis_models.PointField(geography=True, null=True, blank=True)
    dropoff_location = gis_models.PointField(geography=True, null=True, blank=True)
    current_location = gis_models.PointField(geography=True, null=True, blank=True)

    status = models.CharField(
        choices=[
            ("Placed", "Placed"),
            ("Pending", "Pending"),
            ("Accepted", "Accepted"),
            ("Being Prepared", "Being Prepared"),
            ("On the way", "On the way"),
            ("Delivered", "Delivered"),
        ],
        default="Placed",
        max_length=30,
    )
    date_ordered = models.DateField(null=True, blank=True)
    date_delivered = models.DateField(null=True, blank=True)
    payment_method = models.CharField(
        choices=[
            ("Credit Card", "Credit Card"),
            ("Cash in hand", "Cash in hand"),
            ("Paypal", "Paypal"),
            ("Bank Transfer", "Bank Transfer"),
        ],
        default="Cash in hand",
        max_length=100,
    )
    payment_status = models.CharField(
        choices=[
            ("Pending", "Pending"),
            ("Complete", "Complete"),
        ],
        default="Pending",
        max_length=30,
    )
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_totals(self):
        items_total = sum([item.total_price for item in self.items.all()])
        self.total = items_total + self.delivery_fee + self.platform_fee + self.tax
        self.save()

    def clean(self):
        if not self.restaurant and not self.branch:
            raise ValidationError("Either restaurant or branch must be provided.")
        if self.restaurant and self.branch:
            raise ValidationError(
                "Order can only be linked to one of restaurant or branch."
            )

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # price snapshot
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.food.name}"
