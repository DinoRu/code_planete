from django.urls import path
from android import views


app_name = 'android'

urlpatterns = [
    path('', views.AndroidListView.as_view(), name='android-home'),
    path('<int:pk>/', views.android_detail, name='android-detail'),
   #path('tag/<slug:tag_slug>/', views.article_list_by_category, name='article_list_by_tag'),
    path('comment/reply/', views.reply_page, name='reply'),
]