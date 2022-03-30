


from django.urls import path
from pythonbasic import views


app_name = 'pythonbasic'

urlpatterns = [
    path('', views.PythonListView.as_view(), name='home'),
    path('<int:pk>/', views.article_detail, name='article-detail'),
    path('comment/reply/', views.reply_page, name='reply'),
]