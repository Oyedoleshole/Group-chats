# Generated by Django 3.2.4 on 2024-01-19 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=250)),
                ('message', models.TextField()),
                ('thread_name', models.CharField(blank=True, max_length=200, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatapp.room')),
            ],
        ),
    ]
