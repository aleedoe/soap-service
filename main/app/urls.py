from django.urls import path
from .views import soap_service_view

urlpatterns = [
    path('soap/', soap_service_view, name='soap_service'),
]
