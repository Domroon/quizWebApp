# Generated by Django 4.2.4 on 2023-08-31 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_remove_round_statistic_round_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
