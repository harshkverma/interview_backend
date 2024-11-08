from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegistrationSerializer, InterviewSerializer, RoleSerializer
from .models import User, Interview, Roles
from django.utils import timezone
import datetime

class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            # Return serializer errors for better debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "department": user.department,
                    "role": user.role
                },
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleInterviewAPI(generics.CreateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

class AllInterviewsAPI(generics.ListAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

class InterviewsByDateAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        return Interview.objects.filter(date=date)

class InterviewsByWeekAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)  # Sunday

        return Interview.objects.filter(
            date__gte=start_of_week,
            date__lte=end_of_week
        )

class InterviewsByWorkWeekAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=4)  # Friday

        return Interview.objects.filter(
            date__gte=start_of_week,
            date__lte=end_of_week
        )

class InterviewsByMonthAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)  # First day of the current month
        # Calculate the last day of the month
        next_month = start_of_month + datetime.timedelta(days=31)
        start_of_next_month = next_month.replace(day=1)
        end_of_month = start_of_next_month - datetime.timedelta(days=1)  # Last day of the current month

        return Interview.objects.filter(
            date__gte=start_of_month,
            date__lte=end_of_month
        )
    
class GetRolesView(generics.ListAPIView):
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Roles.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "roles": serializer.data,
            "message": "Roles retrieved successfully"
        }, status=status.HTTP_200_OK)
    
class InterviewsByDepartmentAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        department = self.request.query_params.get('department')
        if department:
            return Interview.objects.filter(department=department)
        return Interview.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "interviews": serializer.data,
        }, status=status.HTTP_200_OK)

class GetUpdateDestroyInterviewAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def delete(self, request, *args, **kwargs):
        """Customized delete response to confirm deletion"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Interview deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """Customized update response to provide feedback"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Interview updated successfully",
            "interview": serializer.data
        }, status=status.HTTP_200_OK)
