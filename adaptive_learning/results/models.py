from django.db import models
from django.utils import timezone

class ExamResult(models.Model):
    student        = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='results')
    exam           = models.ForeignKey('exams.Exam', on_delete=models.CASCADE, related_name='results')
    total_marks    = models.PositiveIntegerField()
    marks_obtained = models.PositiveIntegerField(default=0)
    percentage     = models.FloatField(default=0.0)
    status         = models.CharField(max_length=4, choices=[('pass','Pass'),('fail','Fail')])
    started_at     = models.DateTimeField()
    submitted_at   = models.DateTimeField(auto_now_add=True)
    time_taken_min = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student.username} | {self.exam.title} | {self.percentage:.1f}%"

    def calculate_result(self):
        self.percentage = (self.marks_obtained / self.total_marks) * 100
        self.status = 'pass' if self.marks_obtained >= self.exam.pass_marks else 'fail'
        self.save()


class StudentAnswer(models.Model):
    result          = models.ForeignKey(ExamResult, on_delete=models.CASCADE, related_name='answers')
    question        = models.ForeignKey('exams.Question', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')], blank=True)
    is_correct      = models.BooleanField(default=False)
    marks_awarded   = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.result.student.username} | {'✓' if self.is_correct else '✗'}"

    def evaluate(self):
        self.is_correct = (self.selected_option == self.question.correct_answer)
        self.marks_awarded = self.question.marks if self.is_correct else 0
        self.save()


class Payment(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('success','Success'),('failed','Failed')]
    METHOD_CHOICES = [('upi','UPI'),('card','Card'),('netbanking','Net Banking')]

    student        = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='payments')
    course         = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='payments')
    amount         = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=12, choices=METHOD_CHOICES, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    paid_at        = models.DateTimeField(blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} | ₹{self.amount} | {self.status}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('exam','Exam Alert'),('result','Result'),
        ('enrollment','Enrollment'),('payment','Payment'),('general','General')
    ]
    user       = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    title      = models.CharField(max_length=200)
    message    = models.TextField()
    notif_type = models.CharField(max_length=12, choices=TYPE_CHOICES, default='general')
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"