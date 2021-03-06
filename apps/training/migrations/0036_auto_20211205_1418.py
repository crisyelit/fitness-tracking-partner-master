# Generated by Django 3.2 on 2021-12-05 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0035_auto_20211124_0018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='resources',
        ),
        migrations.AlterField(
            model_name='exercise',
            name='warnings',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='resources',
            field=models.ManyToManyField(blank=True, to='training.Resource'),
        ),
    ]
