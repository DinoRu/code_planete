# Generated by Django 4.0.1 on 2022-03-12 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonbasic', '0009_commentarticle_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentarticle',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]