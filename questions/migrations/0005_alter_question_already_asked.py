# Generated by Django 4.2.4 on 2023-08-29 11:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0004_alter_question_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='already_asked',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]