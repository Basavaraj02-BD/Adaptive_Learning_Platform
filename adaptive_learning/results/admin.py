from django.contrib import admin
from .models import ExamResult, StudentAnswer, Payment, Notification

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'total_marks', 'percentage', 'status', 'submitted_at')
    list_filter = ('status',)

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('result', 'question', 'selected_option', 'is_correct', 'marks_awarded')
    list_filter = ('is_correct',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notif_type', 'is_read', 'created_at')
    list_filter = ('notif_type', 'is_read')