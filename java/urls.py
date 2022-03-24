from django.urls import path
from java import views


app_name = 'java'

urlpatterns = [
    #path('', views.JavaListView.as_view(), name='java-home'),
    path('', views.post_list, name='java-home'),
    path('<int:pk>/', views.java_detail, name='java-detail'),
    path('comment/reply/', views.reply_page, name='reply'),
]