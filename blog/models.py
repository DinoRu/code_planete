from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug])


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    titre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = RichTextUploadingField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='img/', blank=True)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month,
                                                 self.publish.day, self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='img/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdf_file/', blank=True, max_length=250)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title}  - {self.author}'


class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f'{self.email}'
