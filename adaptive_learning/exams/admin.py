from django.contrib import admin
from .models import Exam, Question

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'exam_type', 'total_marks', 'pass_marks', 'duration_min', 'is_published')
    list_filter = ('exam_type', 'is_published')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exam', 'correct_answer', 'marks', 'difficulty')
    list_filter = ('difficulty',)
    search_fields = ('question_text',)