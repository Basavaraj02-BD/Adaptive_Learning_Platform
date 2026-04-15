from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from courses.models import Course, Enrollment
from exams.models import Exam
from results.models import Notification


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        role       = request.POST.get('role')
        phone      = request.POST.get('phone')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'accounts/register.html')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role,
            phone=phone
        )
        messages.success(request, 'Account created! Please login.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]

    if user.is_student():
        enrolled_courses = Enrollment.objects.filter(student=user)
        available_exams  = Exam.objects.filter(is_published=True)
        context = {
            'enrolled_courses': enrolled_courses,
            'available_exams': available_exams,
            'notifications': notifications,
            'total_enrolled': enrolled_courses.count(),
        }
        return render(request, 'accounts/student_dashboard.html', context)

    elif user.is_teacher():
        my_courses = Course.objects.filter(teacher=user)
        my_exams   = Exam.objects.filter(created_by=user)
        context = {
            'my_courses': my_courses,
            'my_exams': my_exams,
            'notifications': notifications,
            'total_courses': my_courses.count(),
            'total_exams': my_exams.count(),
        }
        return render(request, 'accounts/teacher_dashboard.html', context)

    else:
        return redirect('/admin/')