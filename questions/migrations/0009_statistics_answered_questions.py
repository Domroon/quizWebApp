# Generated by Django 4.2.4 on 2023-08-29 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_remove_statistics_answered_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='answered_questions',
            field=models.ManyToManyField(to='questions.question'),
        ),
    ]
