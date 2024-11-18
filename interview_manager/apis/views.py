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
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        # If month and year are provided in the query parameters, filter based on them
        if month and year:
            try:
                month = int(month)
                year = int(year)

                # Check if the month and year are valid
                if month < 1 or month > 12:
                    return Response({
                        "error": "Month must be between 1 and 12."
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Calculate the start and end dates of the month
                start_date = datetime.date(year, month, 1)
                if month == 12:
                    end_date = datetime.date(year + 1, 1, 1)  # January of the next year
                else:
                    end_date = datetime.date(year, month + 1, 1)  # First day of the next month

                # Filter interviews based on the calculated range
                return Interview.objects.filter(date__range=[start_date, end_date])

            except ValueError:
                return Response({
                    "error": "Invalid year or month format. Both must be integers."
                }, status=status.HTTP_400_BAD_REQUEST)

        # If no month and year are provided, default to the current month
        else:
            today = timezone.now().date()
            start_of_month = today.replace(day=1)  # First day of the current month
            # Calculate the last day of the current month
            next_month = start_of_month + datetime.timedelta(days=31)
            start_of_next_month = next_month.replace(day=1)
            end_of_month = start_of_next_month - datetime.timedelta(days=1)  # Last day of the current month

            # Return interviews for the current month
            return Interview.objects.filter(
                date__gte=start_of_month,
                date__lte=end_of_month
            )

class InterviewsByDateRangeAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                # Convert to date objects
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

                return Interview.objects.filter(date__range=[start_date, end_date])

            except ValueError:
                return Response({
                    "error": "Invalid date format. Use YYYY-MM-DD."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Interview.objects.none()

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
