from django.urls import path
from . import views

app_name = 'mailer'

urlpatterns = [
    path('', views.mailer_landing_view, name='mailer_landing'),
    path('add-sender/', views.add_sender_view, name='add_sender'),
    path('sender-success/', views.sender_success_view, name='sender_success'),
    path('single-recipient/', views.single_recipient_mailing_view, name='single_recipient_mailing'),
    path('update-sender/<int:sender_id>/', views.update_sender_view, name='update_sender'),
    path('delete-sender/<int:sender_id>/', views.delete_sender_view, name='delete_sender'),
    path('get-sender/<int:sender_id>/', views.get_sender_view, name='get_sender'),
]