from django.urls import path
from . import views

urlpatterns = [
    # ... your other URLs ...
    path('process-payment/', views.process_payment, name='process-payment'),
]