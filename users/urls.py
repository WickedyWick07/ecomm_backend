from django.urls import path
from .views import register, login, logout, user_detail
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('user/', user_detail, name='user_detail'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]