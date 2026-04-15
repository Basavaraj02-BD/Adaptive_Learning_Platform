from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import Exam, Question
from results.models import ExamResult, StudentAnswer, Notification
import random


@login_required
def exam_list(request):
    exams = Exam.objects.filter(is_published=True)
    return render(request, 'exams/exam_list.html', {'exams': exams})


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    already_attempted = ExamResult.objects.filter(
        student=request.user, exam=exam).exists()
    return render(request, 'exams/exam_detail.html', {
        'exam': exam,
        'already_attempted': already_attempted,
        'is_active': exam.is_active(),
    })


@login_required
def start_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk, is_published=True)

    if ExamResult.objects.filter(student=request.user, exam=exam).exists():
        messages.warning(request, 'You have already attempted this exam!')
        return redirect('exam_detail', pk=pk)

    if not exam.is_active():
        messages.error(request, 'This exam is not currently active!')
        return redirect('exam_detail', pk=pk)

    questions = list(exam.questions.all())
    if exam.shuffle_questions:
        random.shuffle(questions)

    request.session[f'exam_{pk}_start'] = timezone.now().isoformat()
    request.session[f'exam_{pk}_questions'] = [q.id for q in questions]

    return render(request, 'exams/take_exam.html', {
        'exam': exam,
        'questions': questions,
        'duration_seconds': exam.duration_min * 60,
    })


@login_required
@transaction.atomic
def submit_exam(request, pk):
    if request.method != 'POST':
        return redirect('exam_list')

    exam = get_object_or_404(Exam, pk=pk)

    if ExamResult.objects.filter(student=request.user, exam=exam).exists():
        messages.warning(request, 'You have already submitted this exam!')
        return redirect('exam_detail', pk=pk)

    start_time_str = request.session.get(f'exam_{pk}_start')
    start_time = timezone.now()
    if start_time_str:
        from datetime import datetime
        start_time = datetime.fromisoformat(start_time_str)
        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)

    time_taken = int((timezone.now() - start_time).total_seconds() / 60)

    # ── Create result record ──────────────────────────────────
    result = ExamResult.objects.create(
        student=request.user,
        exam=exam,
        total_marks=exam.total_marks,
        marks_obtained=0,
        percentage=0.0,
        status='fail',
        started_at=start_time,
        time_taken_min=time_taken,
    )

    # ── Auto Evaluation ───────────────────────────────────────
    total_scored = 0
    questions = exam.questions.all()

    for question in questions:
        selected = request.POST.get(f'question_{question.id}', '')
        is_correct = selected == question.correct_answer
        marks_awarded = question.marks if is_correct else 0
        total_scored += marks_awarded

        StudentAnswer.objects.create(
            result=result,
            question=question,
            selected_option=selected,
            is_correct=is_correct,
            marks_awarded=marks_awarded,
        )

    # ── Update result with final score ────────────────────────
    result.marks_obtained = total_scored
    result.percentage = round((total_scored / exam.total_marks) * 100, 2)
    result.status = 'pass' if total_scored >= exam.pass_marks else 'fail'
    result.save()

    # ── Send notification ─────────────────────────────────────
    Notification.objects.create(
        user=request.user,
        title='Exam Result Published',
        message=f'You scored {total_scored}/{exam.total_marks} ({result.percentage}%) in {exam.title}. Status: {result.status.upper()}',
        notif_type='result'
    )

    # ── Clean session ─────────────────────────────────────────
    request.session.pop(f'exam_{pk}_start', None)
    request.session.pop(f'exam_{pk}_questions', None)

    messages.success(request, f'Exam submitted! You scored {total_scored}/{exam.total_marks}')
    return redirect('result_detail', pk=result.pk)


@login_required
def create_exam(request):
    if not request.user.is_teacher():
        messages.error(request, 'Only teachers can create exams!')
        return redirect('dashboard')

    from courses.models import Course
    courses = Course.objects.filter(teacher=request.user)

    if request.method == 'POST':
        exam = Exam.objects.create(
            title=request.POST.get('title'),
            course=__import__('courses').models.Course.objects.get(
                pk=request.POST.get('course')),
            exam_type=request.POST.get('exam_type', 'mcq'),
            total_marks=request.POST.get('total_marks', 100),
            pass_marks=request.POST.get('pass_marks', 40),
            duration_min=request.POST.get('duration_min', 60),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            is_published=True,
            created_by=request.user,
        )
        messages.success(request, f'Exam "{exam.title}" created! Now add questions.')
        return redirect('add_question', pk=exam.pk)

    return render(request, 'exams/create_exam.html', {'courses': courses})


@login_required
def add_question(request, pk):
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)
    if request.method == 'POST':
        Question.objects.create(
            exam=exam,
            question_text=request.POST.get('question_text'),
            option_a=request.POST.get('option_a'),
            option_b=request.POST.get('option_b'),
            option_c=request.POST.get('option_c', ''),
            option_d=request.POST.get('option_d', ''),
            correct_answer=request.POST.get('correct_answer'),
            marks=request.POST.get('marks', 1),
            difficulty=request.POST.get('difficulty', 'medium'),
            explanation=request.POST.get('explanation', ''),
        )
        if request.POST.get('add_more'):
            messages.success(request, 'Question added! Add another.')
            return redirect('add_question', pk=pk)
        messages.success(request, 'All questions saved!')
        return redirect('exam_detail', pk=pk)

    questions = exam.questions.all()
    return render(request, 'exams/add_question.html', {
        'exam': exam,
        'questions': questions,
    })
