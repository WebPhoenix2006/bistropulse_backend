from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_franchise_id():
    last_id = Franchise.objects.all().order_by("id").last()
    number = int(last_id.franchise_id[2:]) + 1 if last_id else 1
    return f"BF{number:04d}"


def generate_branch_id():
    last_id = Branch.objects.all().order_by("id").last()
    number = int(last_id.branch_id[3:]) + 1 if last_id else 1
    return f"BFb{number:04d}"


class Representative(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    representative_image = models.ImageField(
        upload_to="representatives/", blank=True, null=True
    )

    def __str__(self):
        return self.full_name


class Franchise(models.Model):
    franchise_id = models.CharField(
        max_length=10, unique=True, default=generate_franchise_id, editable=False
    )
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Representative, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20)
    business_license = models.FileField(
        upload_to="licenses/franchise/", blank=True, null=True
    )
    owner_nid = models.FileField(upload_to="nid/franchise/", blank=True, null=True)
    established_date = models.DateField()
    franchise_image = models.ImageField(upload_to="franchise/", blank=True, null=True)
    overall_rating = models.CharField(max_length=5, default="0.0")
    status = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="franchises", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    branch_id = models.CharField(
        max_length=10, unique=True, default=generate_branch_id, editable=False
    )
    franchise = models.ForeignKey(
        Franchise, on_delete=models.CASCADE, related_name="branches"
    )
    name = models.CharField(max_length=255)
    representative = models.ForeignKey(
        Representative, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone = models.CharField(max_length=20)
    business_license = models.FileField(
        upload_to="licenses/branch/", blank=True, null=True
    )
    owner_nid = models.FileField(upload_to="nid/branch/", blank=True, null=True)
    established_date = models.DateField()
    working_period = models.CharField(max_length=255)
    large_option = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    restaurant_image = models.ImageField(upload_to="branches/", blank=True, null=True)
    rating = models.CharField(max_length=5, default="0.0")
    status = models.CharField(
        max_length=20, choices=[("Open", "Open"), ("Closed", "Closed")], default="Open"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="branches", blank=True, null=True
    )

    def __str__(self):
        return self.name
