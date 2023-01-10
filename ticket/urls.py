from django.urls import path
from . import views
app_name = 'ticket'

urlpatterns = [
    path('create_ticket/', views.create_ticket),
    path('show_all_ticket/', views.show_all_ticket),
    path('show_single_ticket/', views.show_single_ticket),
]
