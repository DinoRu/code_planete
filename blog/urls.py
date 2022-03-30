from django.urls import path

from blog import views
from blog.feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list_by_category, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name="post_share"),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('about/', views.about, name='about'),
    path('about_site/', views.about_site, name='about_site'),
    path('book_list/', views.BookListView.as_view(), name='book_list'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('<slug:category_slug>/', views.post_list_by_category, name='post_list_by_category'),
    path('<int:pk>/download_image/', views.download_idea_picture, name='download_book_image'),
    path('comment/reply/', views.reply, name='reply'),
]