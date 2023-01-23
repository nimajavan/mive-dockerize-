from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('products_list/', views.get_product_list),
    path('product_info/<slug>/', views.get_product_info),
    path('product_comments/', views.get_product_comments),
    path('send_comment/', views.send_comment),
    path('like/', views.Like.as_view())
]
