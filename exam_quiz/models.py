from django.db import models
from django.contrib.auth.models import User  # <--- YE IMPORT ZAROORI HAI

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_marks = models.IntegerField()

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

# Isse Question class ke bahar likhna (No indentation)
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_attempted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"