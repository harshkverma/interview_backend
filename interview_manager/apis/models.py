from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid

# Choices for department and role
Department_Choice = (
    ("Software", "Software"),
    ("Testing", "Testing"),
    ("Cyber-Security", "Cyber-Security"),
    ("Finance", "Finance")
)

Role_Choice = (
    ("Manager", "Manager"),
    ("Senior", "Senior"),
    ("Junior", "Junior"),
    ("Team Lead", "Team Lead"),
    ("Intern", "Intern")
)

class UserManager(BaseUserManager):
    def create_user(self, email, password, department, role, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,department=department, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    department = models.CharField(max_length=20, choices=Department_Choice)
    role = models.CharField(max_length=10, choices=Role_Choice)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

class Interviewee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Interview(models.Model):
    interviewee = models.ForeignKey(Interviewee, on_delete=models.CASCADE)
    interview_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    role = models.CharField(max_length=50, choices=Role_Choice)
    interviewer_name = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100)
    business_area = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=Department_Choice)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.interviewee} - {self.interview_id}"

class Roles(models.Model):
    job_title = models.CharField(max_length=50)

    def __str__(self):
        return self.job_title