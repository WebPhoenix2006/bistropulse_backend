import random
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_custom_id():
    return f"B{random.randint(1000, 9999)}"

class Restaurant(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=5,
        unique=True,
        editable=False,
        default=generate_custom_id
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    representative = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(max_length=10, choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Closed')

    def __str__(self):
        return self.name
    def generate_unique_id():
        while True:
            new_id = f"B{random.randint(1000, 9999)}"
            if not Restaurant.objects.filter(id=new_id).exists():
                return new_id

    id = models.CharField(
    primary_key=True,
    max_length=5,
    unique=True,
    editable=False,
    default=generate_unique_id
)

