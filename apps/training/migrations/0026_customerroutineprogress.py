# Generated by Django 3.2 on 2021-11-19 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0025_auto_20211119_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRoutineProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_exercise', models.IntegerField()),
                ('total_exercise', models.IntegerField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.customerroutine')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.dayroutine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
