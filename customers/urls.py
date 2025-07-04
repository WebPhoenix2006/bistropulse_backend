from django.urls import path
from .views import CustomerDetailView, CustomerListCreateView

urlpatterns = [
    path("", CustomerListCreateView.as_view(), name="customers"),
    path("<str:customer_id>/", CustomerDetailView.as_view(), name="customer-detail"),
]
