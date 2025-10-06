

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=255)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField()
    time_taken = models.CharField(max_length=20)
    difficulty = models.CharField(
        max_length=10, 
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ],
        null=True,
        blank=True
    )
    time_efficiency = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz_name} ({self.score}/{self.total_questions})"

class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name='attempts')
    question = models.TextField()
    user_answer = models.TextField()
    correct_answer = models.TextField()
    is_correct = models.BooleanField()
    time_taken = models.CharField(max_length=20)

    def __str__(self):
        return f"Question {self.id} - {'Correct' if self.is_correct else 'Incorrect'}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    num_questions = models.IntegerField()
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    created_at = models.DateTimeField(auto_now_add=True)
    generated_mcqs = models.TextField(blank=True, null=True)

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.verification_code}"