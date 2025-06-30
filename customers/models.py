from django.db import models
from django.contrib.auth.models import User

import random
import string

def generate_customer_id():
    prefix = 'user#'
    suffix = ''.join(random.choices(string.digits, k=6))
    return f'{prefix}{suffix}'

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')  # <--- Add this line
    customer_id = models.CharField(max_length=10, unique=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_student = models.BooleanField(default=False)
    gender = models.CharField(max_length=10)
    location = models.TextField()
    photo = models.ImageField(upload_to='customer_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            while True:
                new_id = generate_customer_id()
                if not Customer.objects.filter(customer_id=new_id).exists():
                    self.customer_id = new_id
                    break
        super().save(*args, **kwargs)
