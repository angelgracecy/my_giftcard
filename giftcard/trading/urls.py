from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('giftcards/add/', views.add_giftcard, name='add_giftcard'),
    path('giftcards/my/', views.my_giftcards, name='my_giftcards'),
    path('trade/<int:pk>/', views.trade_giftcard, name='trade_giftcard'),
    path('rate/<int:user_id>/', views.rate_user, name='rate_user'),
]
