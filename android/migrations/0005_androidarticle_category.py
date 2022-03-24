# Generated by Django 4.0.1 on 2022-03-12 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_comment_reply'),
        ('android', '0004_alter_commentarticle_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='androidarticle',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='blog.category'),
        ),
    ]