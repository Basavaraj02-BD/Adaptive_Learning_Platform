from django.db import models
from django.utils import timezone

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    thumbnail    = models.ImageField(upload_to='courses/', blank=True, null=True)
    teacher      = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='courses_taught')
    level        = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    price        = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_free      = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course       = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    order        = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} → {self.title}"


class LearningMaterial(models.Model):
    TYPE_CHOICES = [
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('document', 'Document'),
        ('link', 'External Link'),
    ]
    module        = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='materials')
    title         = models.CharField(max_length=200)
    material_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file          = models.FileField(upload_to='materials/', blank=True, null=True)
    url           = models.URLField(blank=True)
    description   = models.TextField(blank=True)
    order         = models.PositiveIntegerField(default=1)
    duration_min  = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} → {self.title}"


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    student     = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='enrollments')
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"


class StudentProgress(models.Model):
    student        = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='progress')
    material       = models.ForeignKey(LearningMaterial, on_delete=models.CASCADE)
    is_completed   = models.BooleanField(default=False)
    completed_at   = models.DateTimeField(blank=True, null=True)
    time_spent_min = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'material')

    def __str__(self):
        return f"{self.student.username} | {self.material.title}"

    def mark_complete(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()