import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .models import JavaArticle, CommentJava
from django.db.models import Count
from blog.models import Category
from .forms import CommentForm
from taggit.models import Tag



def post_list(request, tag_slug=None, category_slug=None):
    now = datetime.datetime.now
    object_list = JavaArticle.published.all()
    tag = None
    category = None
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category__in=[category])
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first in each page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the first page
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'page': page,
        'tag': tag,
        'category': category,
        'categories': categories,
        'now': now,
    }
    return render(request, 'java/java_list.html', context=context)


def java_detail(request, pk):
    article = get_object_or_404(JavaArticle, pk=pk)
    categories = Category.objects.all()
    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            return redirect(article.get_absolute_url()+'#'+str(new_comment.id))

    else:
        comment_form = CommentForm()

    post_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = JavaArticle.published.filter(tags__in=post_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'similar_articles': similar_articles,
        'categories': categories,
    }
    return render(request, 'java/java_detail.html', context)


def reply_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            article_id = request.POST.get('article_id')
            parent_id = request.POST.get('parent')
            article_url = request.POST.get('article_url')

            reply = form.save(commit=False)
            reply.article = JavaArticle(id=article_id)
            reply.parent = CommentJava(id=parent_id)
            reply.save()
            
            return redirect(article_url+'#'+str(reply.id))

    return redirect("/")