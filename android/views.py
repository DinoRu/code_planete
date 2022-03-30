import datetime
from re import T
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView
from django.db.models import Count
from .models import AndroidArticle, CommentArticle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Category
from .forms import CommentForm
from taggit.models import Tag


class AndroidListView(ListView):
    model = AndroidArticle
    paginate_by = 6
    template_name = "android/android_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['android_articles'] = AndroidArticle.published.all()
        context['categories'] = Category.objects.all()
        return context



def android_detail(request, pk):
    article = get_object_or_404(AndroidArticle, pk=pk)
    categories = Category.objects.all()
    
    # Liste de commentaire active pour chaque article
    comments = article.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Creer un objet CommentArticle mais ne sauvegardez pas
            new_comment = comment_form.save(commit=False)
            # Faire correspondre l'article correspond au commentaie
            new_comment.article = article
            # Sauvegarder le commentaire de cet article
            new_comment.save()
            # redirectiion sur la meme page
            return redirect(article.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()

    post_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = AndroidArticle.published.filter(tags__in=post_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
        'similar_articles': similar_articles,
    }
    return render(request, 'android/android_detail.html', context)


def reply_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            article_id = request.POST.get('article_id')
            parent_id = request.POST.get('parent')
            article_url = request.POST.get('article_url')

            reply = form.save(commit=False)
            reply.article = AndroidArticle(id=article_id)
            reply.parent = CommentArticle(id=parent_id)
            reply.save()

            return redirect(article_url+'#'+str(reply.id))

    return redirect("/")