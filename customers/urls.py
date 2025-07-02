from django.urls import path
from .views import CustomerDetailView, CustomerListCreateView

urlpatterns = [
    path('', CustomerListCreateView.as_view(), name='customers'),
    path('customers/<int:pk>/', CustomerDetailView.as_view()),  # 👈 dynamic route

]
