from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Picture(BaseModel):
    name = models.CharField(max_length=30, default="unnamed")
    image = models.ImageField(null=True, blank=False, upload_to="media")
    description = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(BaseModel):
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

    def clear_already_asked(self):
        self.already_asked.clear()
        self.save()

        
class BasicAnswer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=False)
    answer_text = models.CharField(max_length=60, null=True, blank=True)
    explanation = models.CharField(max_length=60, null=True, blank=True)
    is_true = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.question.question_text} - {self.answer_text} - {self.is_true}'


class Statistic(BaseModel):
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=False, on_delete=models.CASCADE)
    right_answered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - Total: {self.answered_questions_count} - Right: {self.right_answers_count}'


class Round(BaseModel):
    MODIS = [
        ("M", "MIXED"),
        ("T", "TOPIC")
    ]
    modus = models.CharField(max_length=1, choices=MODIS, null=True, blank=False)
    questions = models.ManyToManyField(Question)
    answered_questions_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.modus} - {self.user.username} - {self.created_at}'


admin.site.register(Picture)
admin.site.register(Question)
admin.site.register(BasicAnswer)
admin.site.register(Round)
admin.site.register(Statistic)