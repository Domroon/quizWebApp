# Generated by Django 4.2.4 on 2023-08-29 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_alter_question_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statistics',
            name='answered_questions',
        ),
    ]