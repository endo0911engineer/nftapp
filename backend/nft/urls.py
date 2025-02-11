from django.urls import path
from . import views

urlpatterns = [
    path('send_gift/', views.send_gift, name="send_gift"),
    path('received_gifts/', views.received_gifts, name='received_gifts'),
    path('confirm_gift/', views.confirm_gift, name='confirm_gift'),
    path('mint_nft/', views.mint_nft, name='mint_nft'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('get_sign_message/', views.get_sign_message, name='get_sign_message'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('check_authentication/', views.check_authentication, name='check_authentication'),
]