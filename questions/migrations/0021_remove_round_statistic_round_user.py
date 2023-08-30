# Generated by Django 4.2.4 on 2023-08-30 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0020_remove_round_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='statistic',
        ),
        migrations.AddField(
            model_name='round',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]