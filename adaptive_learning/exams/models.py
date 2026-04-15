from django.db import models
from django.utils import timezone

class Exam(models.Model):
    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True / False'),
        ('mixed', 'Mixed'),
    ]
    course            = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='exams')
    title             = models.CharField(max_length=200)
    description       = models.TextField(blank=True)
    exam_type         = models.CharField(max_length=12, choices=TYPE_CHOICES, default='mcq')
    total_marks       = models.PositiveIntegerField(default=100)
    pass_marks        = models.PositiveIntegerField(default=40)
    duration_min      = models.PositiveIntegerField(default=60)
    start_time        = models.DateTimeField()
    end_time          = models.DateTimeField()
    is_published      = models.BooleanField(default=False)
    shuffle_questions = models.BooleanField(default=True)
    created_by        = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='exams_created')
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time and self.is_published


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    exam           = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text  = models.TextField()
    option_a       = models.CharField(max_length=300)
    option_b       = models.CharField(max_length=300)
    option_c       = models.CharField(max_length=300, blank=True)
    option_d       = models.CharField(max_length=300, blank=True)
    correct_answer = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    marks          = models.PositiveIntegerField(default=1)
    difficulty     = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default='medium')
    explanation    = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question_text[:60]}"