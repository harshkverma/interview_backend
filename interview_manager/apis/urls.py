from django.urls import path
from .views import LoginUserView, RegisterUserView

urlpatterns = [
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
]
