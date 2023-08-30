# Generated by Django 4.2.4 on 2023-08-30 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0019_alter_basicanswer_answer_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='user',
        ),
        migrations.RemoveField(
            model_name='statistic',
            name='answered_questions_count',
        ),
        migrations.RemoveField(
            model_name='statistic',
            name='right_answers_count',
        ),
        migrations.AddField(
            model_name='round',
            name='answered_questions_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistic',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.question'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='right_answered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statistic',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]