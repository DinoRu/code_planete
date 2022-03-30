import os.path
import datetime
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView
from blog.forms import EmailPostForm, CommentForm, SearchForm, SubscribeForm
from blog.models import Post, Comment, Category, Book
from taggit.models import Tag
from blog.documents import PostDocument, CategoryDocument


def post_list(request, tag_slug=None, category_slug=None):
    now = datetime.datetime.now
    object_list = Post.published.all()
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
    return render(request, 'blog/posts/list.html', context=context)


def post_list_by_category(request, category_slug=None, tag_slug=None):
    now = datetime.datetime.now
    object_list = Post.published.all()
    categories = Category.objects.all()
    category = None
    tag = None
    author = None
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
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'categories': categories,
        'category': category,
        'posts': posts,
        'page': page,
        'tag': tag,
        'author': author,
        'now': now,
    }
    return render(request, 'blog/posts/post_list_category.html', context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    categories = Category.objects.all()
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'categories': categories,
    }
    return render(request, 'blog/posts/detail.html', context=context)


def reply(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent')
            post_url = request.POST.get('post_url')

            reply = form.save(commit=False)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url+'#'+str(reply.id))
    return redirect('/')


def post_share(request, post_id):
    # Recuperer un post par son identifiant
    post = get_object_or_404(Post, id=post_id, status='published')
    categories = Category.objects.all()
    sent = False
    if request.method == 'POST':
        # Formulaire a ete soumis
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # formulaire est valide
            cd = form.cleaned_data
            # email envoyé
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommands you read"\
                        f"{post.titre}"
            message = f"Read {post.titre} at {post_url}\n\n"\
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'diarra.msa1@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    # La liste des posts similaires
    context = {
        'post': post,
        'form': form,
        'sent': sent,
        'categories': categories,
    }
    return render(request, 'blog/posts/share.html', context=context)


def post_search(request, tag_slug=None):
    categories = Category.objects.all()
    object_list = Post.published.all()
    form = SearchForm()
    query = request.GET.get('query')
    tag = None
    results = []
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    if query:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.filter(Q(titre__icontains=query) | Q(body__icontains=query))
    context = {
        'form': form,
        'query': query,
        'results': results,
        'categories': categories,
        'tag': tag,
        'object_list': object_list,
        'posts': posts,
        'page': page,
    }
    return render(request, 'blog/posts/search.html', context=context)


def about(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'blog/posts/about.html', context=context)


def about_site(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'blog/posts/about_site.html', context=context)


class BookListView(ListView):
    
    model = Book
    template_name = 'blog/posts/book_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context


def download_idea_picture(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.pdf:
        filename, extension = os.path.splitext(book.pdf.file.name)
        extension = extension[1:]
        response = FileResponse(
            book.pdf.file, content_type=f"image/{extension}"
        )
        slug = slugify(book.title)[:100]
        response["Content-Disposition"] = (
            "attachement; filename="
            f"{slug}.{extension}"
        )
    else:
        response = HttpResponseNotFound(
            content="file invalide"
        )
    return response


def subscribe(request):
    my_form = SubscribeForm()
    if request.method == 'POST':
        my_form = SubscribeForm(data=request.POST or None)
        if my_form.is_valid():
            cd = my_form.cleaned_data
            my_form.save()
            return redirect('blog:book_list')
        else:
            my_form = SubscribeForm()
    else:
        my_form = SubscribeForm()
    return render(request, 'blog/posts/subscribe_email.html', {'my_form': my_form})
