# Generated by Django 4.0.1 on 2022-01-21 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pdf',
            field=models.FileField(blank=True, upload_to='pdf_file/'),
        ),
    ]