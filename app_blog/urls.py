from django.test import TestCase
from django.urls import path

from app_blog import views

app_name = 'blog'
urlpatterns = [
    path('articles/', views.ArticleView.as_view()),
    path('articles/<int:article_id>/', views.ArticleView.as_view()),
]
