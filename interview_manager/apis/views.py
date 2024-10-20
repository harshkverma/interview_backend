from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegistrationSerializer, InterviewSerializer, RoleSerializer
from .models import User, Interview, Roles
from django.utils import timezone

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
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        return Interview.objects.filter(date__range=[start_date, end_date])

class InterviewsByWorkWeekAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        return Interview.objects.filter(date__range=[start_date, end_date]).exclude(date__week_day__in=[7, 1])

class InterviewsByMonthAPI(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        return Interview.objects.filter(date__month=month, date__year=year)
    
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