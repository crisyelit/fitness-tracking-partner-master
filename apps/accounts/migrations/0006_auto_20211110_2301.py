# Generated by Django 3.2 on 2021-11-11 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_user_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enable_nutrition',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='enable_tracking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='enable_training',
            field=models.BooleanField(default=False),
        ),
    ]
