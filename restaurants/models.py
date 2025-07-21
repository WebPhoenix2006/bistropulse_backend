from django.utils import timezone
import random
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


def generate_unique_id():
    while True:
        new_id = f"B{random.randint(1000, 9999)}"
        if not Restaurant.objects.filter(id=new_id).exists():
            return new_id


class Representative(models.Model):
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="restaurant_rep_images/", null=True, blank=True)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Restaurant(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=5,
        unique=True,
        editable=False,
        default=generate_unique_id,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurants"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    representative = models.ForeignKey(
        Representative,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurants",
    )
    phone = models.CharField(max_length=20)
    business_license = models.FileField(upload_to="licenses/", null=True, blank=True)
    owner_nid = models.FileField(upload_to="nid/", null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)
    working_period = models.CharField(max_length=30, null=True, blank=True)
    large_option = models.CharField(max_length=30, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    restaurant_image = models.ImageField(
        upload_to="restaurant_images/", null=True, blank=True
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(
        max_length=10,
        choices=[("Open", "Open"), ("Closed", "Closed")],
        default="Closed",
    )

    def __str__(self):
        return self.name or self.id


class FoodCategory(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="categories", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Extra(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Food(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="foods", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        FoodCategory, related_name="foods", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)
    extras = models.ManyToManyField(Extra, blank=True, related_name="foods")

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="reviews", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}/5"


class Rider(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    profile_image = models.ImageField(
        upload_to="rider_profiles/", null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="riders"
    )
    is_active = models.BooleanField(default=True)
    rider_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.rider_code:
            code = f"R{random.randint(1000, 9999)}"
            while Rider.objects.filter(rider_code=code).exists():
                code = f"R{random.randint(1000, 9999)}"
            self.rider_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class ShiftType(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class RiderShift(models.Model):
    SHIFT_STATUS = (
        ("started", "Started"),
        ("ended", "Ended"),
        ("cancelled", "Cancelled"),
    )

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name="shifts")
    shift_type = models.ForeignKey(ShiftType, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    secret_code = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=10, choices=SHIFT_STATUS, default="started")
    started_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="shifts_started"
    )
    ended_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shifts_ended",
    )

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        return f"{self.rider.full_name} - {self.status} - {self.start_time.date()}"


def generate_order_id():
    while True:
        order_id = f"BO{random.randint(1000, 9999)}"
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("pickoff", "Pickoff"),
        ("dropoff", "Dropoff"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("paid", "Paid"),
        ("not_paid", "Not Paid"),
    ]

    order_id = models.CharField(
        max_length=10, unique=True, default=generate_order_id, editable=False
    )
    restaurant = models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='not_paid')

    delivery_address = models.TextField(blank=True, null=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.name} (₦{self.unit_price})"
