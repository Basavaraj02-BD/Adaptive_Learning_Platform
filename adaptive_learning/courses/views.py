from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, LearningMaterial, Enrollment, StudentProgress


def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course  = get_object_or_404(Course, pk=pk)
    modules = course.modules.filter(is_published=True)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
    })


@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not request.user.is_student():
        messages.error(request, 'Only students can enroll!')
        return redirect('course_detail', pk=pk)
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user, course=course)
    if created:
        messages.success(request, f'Successfully enrolled in {course.title}!')
    else:
        messages.info(request, 'You are already enrolled in this course.')
    return redirect('course_detail', pk=pk)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})


@login_required
def create_course(request):
    if not request.user.is_teacher():
        messages.error(request, 'Only teachers can create courses!')
        return redirect('dashboard')
    if request.method == 'POST':
        title       = request.POST.get('title')
        description = request.POST.get('description')
        level       = request.POST.get('level')
        price       = request.POST.get('price', 0)
        is_free     = request.POST.get('is_free') == 'on'
        thumbnail   = request.FILES.get('thumbnail')
        course = Course.objects.create(
            title=title, description=description, level=level,
            price=price, is_free=is_free, teacher=request.user,
            thumbnail=thumbnail, is_published=True
        )
        messages.success(request, f'Course "{course.title}" created successfully!')
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/create_course.html')


@login_required
def add_module(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        order = request.POST.get('order', 1)
        Module.objects.create(
            course=course, title=title,
            description=description, order=order, is_published=True
        )
        messages.success(request, 'Module added successfully!')
        return redirect('course_detail', pk=pk)
    return render(request, 'courses/add_module.html', {'course': course})