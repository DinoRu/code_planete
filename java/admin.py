from django.contrib import admin
from .models import JavaArticle, CommentJava, Category

@admin.register(JavaArticle)
class JavaArticleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'publish', 'author']
    search_fields = ['titre', 'body']
    prepopulated_fields = {'slug': ('titre', )}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(CommentJava)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created',)
    list_filter = ('created',)
    search_fields = ('author', 'body')

admin.site.register(Category)