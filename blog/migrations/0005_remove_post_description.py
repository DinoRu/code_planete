# Generated by Django 4.0.1 on 2022-01-19 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='description',
        ),
    ]
