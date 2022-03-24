from django.contrib import admin
from .models import Article, CommentPython

@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titre', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'publish', 'author']
    search_fields = ['titre', 'body']
    prepopulated_fields = {'slug': ('titre', )}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(CommentPython)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created',)
    list_filter = ('created',)
    search_fields = ('author', 'body')
