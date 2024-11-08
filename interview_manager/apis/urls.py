from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/interview/schedule/', ScheduleInterviewAPI.as_view(), name='schedule-interview'),
    path('api/interview/all/', AllInterviewsAPI.as_view(), name='all-interviews'),
    path('api/interview/date/', InterviewsByDateAPI.as_view(), name='interviews-by-date'),
    path('api/interview/week/', InterviewsByWeekAPI.as_view(), name='interviews-by-week'),
    path('api/interview/work-week/', InterviewsByWorkWeekAPI.as_view(), name='interviews-by-work-week'),
    path('api/interview/month/', InterviewsByMonthAPI.as_view(), name='interviews-by-month'),
    path('api/roles/', GetRolesView.as_view(), name='get-roles'),
    path('api/interview/department/', InterviewsByDepartmentAPI.as_view(), name='interviews-by-department'),
    path('api/interview/<int:pk>/', GetUpdateDestroyInterviewAPI.as_view(), name='retrieve-update-destroy-interview'),
]
