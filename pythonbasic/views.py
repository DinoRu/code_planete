from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView
from pythonbasic.models import Article, CommentPython
from blog.models import Category
from .forms import CommentForm
from django.views.generic.edit import ModelFormMixin, FormMixin


class PythonListView(ListView):
    model = Article
    paginate_by = 6
    template_name = "basic/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['articles'] = Article.published.all()
        context['categories'] = Category.objects.all()
        return context


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
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
    similar_articles = Article.published.filter(tags__in=post_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]   
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
        'similar_articles': similar_articles,
    }
    return render(request, 'basic/article-detail.html', context)


def reply_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            article_id = request.POST.get('article_id')
            parent_id = request.POST.get('parent')
            article_url = request.POST.get('article_url')

            reply = form.save(commit=False)
            reply.article = Article(id=article_id)
            reply.parent = CommentPython(id=parent_id)
            reply.save()
            
            return redirect(article_url+'#'+str(reply.id))
            
    return redirect('/')

