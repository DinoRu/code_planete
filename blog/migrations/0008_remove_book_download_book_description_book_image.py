# Generated by Django 4.0.1 on 2022-01-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_books_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='download',
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/'),
        ),
    ]