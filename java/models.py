from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name



class JavaArticle(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    titre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='java_auteur')
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='img/', blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='draft')
    categories = models.ManyToManyField(Category, related_name='java_articles')
    published = PublishedManager()
    tags = TaggableManager()

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('java:java-detail', args=[str(self.id)])
    
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)


class CommentJava(models.Model):
    article = models.ForeignKey(JavaArticle, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=80)
    email = models.EmailField(max_length=80, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.author} on {self.article.titre}'

    def get_comments(self):
        return CommentJava.objects.filter(parent=self).filter(active=True)

