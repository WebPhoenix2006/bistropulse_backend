from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Restaurant(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    representative = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Closed')
    
    def __str__(self):
        return self.name
