# Generated by Django 5.1.1 on 2024-09-27 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseAlias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=20, verbose_name='課名全稱')),
                ('alias', models.CharField(max_length=20, verbose_name='課程簡稱')),
            ],
        ),
    ]
