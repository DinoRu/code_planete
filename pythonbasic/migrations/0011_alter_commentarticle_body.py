# Generated by Django 4.0.1 on 2022-03-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonbasic', '0010_alter_commentarticle_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentarticle',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
