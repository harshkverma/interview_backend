from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

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
