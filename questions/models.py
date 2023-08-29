from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Picture(models.Model):
    name = models.CharField(max_length=30, default="unnamed")
    image = models.ImageField(null=True, blank=False, upload_to="media")
    description = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPES = [
        ("TR", "Truth"),
        ("MU", "Multi"),
        ("SI", "Single"),
        ("TE", "Text")
    ]
    TOPICS = [
        ("GE", "Geography"),
        ("EN", "Entertainment"),
        ("HI", "History"),
        ("AL", "Art and Literature"),
        ("ST", "Science and Technology"),
        ("SP", "Sports and Pleasure")
    ]
    question_text = models.CharField(max_length=100, null=True, blank=False, unique=True)
    question_type = models.CharField(max_length=2, choices=TYPES, null=True, blank=False)
    reference_link = models.URLField(max_length=200, null=True, blank=True)
    topic = models.CharField(max_length=2, choices=TOPICS, null=True, blank=False)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, null=True, blank=True)
    already_asked = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.question_type} - {self.question_text}'


class TruthAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=False)
    is_true = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.question.question_text} - {self.is_true}'


class BasicAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=False)
    answer_text = models.CharField(max_length=60, null=True, blank=False)
    is_true = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.question.question_text} - {self.answer_text} - {self.is_true}'


class Round(models.Model):
    MODIS = [
        ("M", "MIXED"),
        ("T", "TOPIC")
    ]
    modus = models.CharField(max_length=1, choices=MODIS, null=True, blank=False)
    questions = models.ManyToManyField(Question)
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.modus}'


class Statistics(models.Model):
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    answered_questions_count = models.IntegerField(default=0)
    right_answers_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} - {self.user.username}'


admin.site.register(Picture)
admin.site.register(Question)
admin.site.register(TruthAnswer)
admin.site.register(BasicAnswer)
admin.site.register(Round)
admin.site.register(Statistics)