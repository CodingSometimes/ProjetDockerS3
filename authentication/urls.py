from django.urls import path
from .views import LoginUser, LogoutUser, register

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', register, name='register'),
]
