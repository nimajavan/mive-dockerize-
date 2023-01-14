from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    # admin
    path('get_admin_information/', views.admin_panel_information,
         name='get_admin_information'),
    # admin
    path('phone_register/', views.phone_register),
    path('register/', views.user_register),
    path('update_profile/', views.SetupProfile.as_view()),
    path('login/', views.MyCreatorTokenView.as_view()),
]
