from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile', views.user_profile, name='profile'),
    path('payment/<int:order_id>/', views.complete_payment, name='payment'),
    path('review/add/<int:product_id>/', views.add_review, name='add_review')
]