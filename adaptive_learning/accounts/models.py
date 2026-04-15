from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin',   'Admin'),
    ]
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone       = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_student(self):  return self.role == 'student'
    def is_teacher(self):  return self.role == 'teacher'
