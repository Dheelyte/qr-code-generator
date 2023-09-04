from django.urls import path
from .views import QRGenerator

urlpatterns = [
    path('', QRGenerator.as_view(), name='qr-generator'),
]