# Generated by Django 4.2.4 on 2023-08-30 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0015_rename_questions_answered_counter_round_answered_questions_counter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('answered_questions_count', models.IntegerField(default=0)),
                ('right_answers_count', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Statistics',
        ),
        migrations.AddField(
            model_name='round',
            name='statistic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.statistic'),
        ),
    ]