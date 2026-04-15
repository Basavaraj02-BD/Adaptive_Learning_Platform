from django.contrib import admin
from .models import Course, Module, LearningMaterial, Enrollment, StudentProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'level', 'price', 'is_free', 'is_published', 'created_at')
    list_filter = ('level', 'is_published', 'is_free')
    search_fields = ('title',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_published')
    list_filter = ('is_published',)

@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'material_type', 'order', 'duration_min')
    list_filter = ('material_type',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_at')
    list_filter = ('status',)

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'material', 'is_completed', 'time_spent_min')
    list_filter = ('is_completed',)