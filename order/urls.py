from django.urls import path
from . import views
app_name = 'order'

urlpatterns = [
    path('add_order/', views.GetOrderItem.as_view()),
    path('create_payment_url/', views.create_payment_url),
    path('verify_peyment/', views.payment_return),
    path('check_payment/', views.payment_check),
]
