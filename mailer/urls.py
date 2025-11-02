from django.urls import path
from . import views

urlpatterns = [
    path('add-sender/', views.add_sender_view, name='add_sender'),
    path('sender-success/', views.sender_success_view, name='sender_success'),
]