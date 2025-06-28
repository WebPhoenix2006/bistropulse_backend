import random
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_unique_id():
    while True:
        new_id = f"B{random.randint(1000, 9999)}"
        if not Restaurant.objects.filter(id=new_id).exists():
            return new_id

class Restaurant(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=5,
        unique=True,
        editable=False,
        default=generate_unique_id
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    representative = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    business_license = models.FileField(upload_to='licenses/', null=True, blank=True)
    owner_nid = models.FileField(upload_to='nid/', null=True, blank=True)
    established_date = models.DateField()
    working_period = models.CharField(max_length=30)
    large_option = models.CharField(max_length=30)
    location = models.TextField()
    restaurant_image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(max_length=10, choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Closed')

    def __str__(self):
        return self.name
