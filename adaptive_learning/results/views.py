from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExamResult, Notification


@login_required
def my_results(request):
    results = ExamResult.objects.filter(
        student=request.user).order_by('-submitted_at')
    return render(request, 'results/my_results.html', {'results': results})


@login_required
def result_detail(request, pk):
    result   = get_object_or_404(ExamResult, pk=pk, student=request.user)
    answers  = result.answers.select_related('question').all()
    correct  = answers.filter(is_correct=True).count()
    wrong    = answers.filter(is_correct=False).count()
    return render(request, 'results/result_detail.html', {
        'result':  result,
        'answers': answers,
        'correct': correct,
        'wrong':   wrong,
    })


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'results/notifications.html', {'notifs': notifs})