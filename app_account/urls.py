from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('articles/', views.ArticleProfileView.as_view()),
    path('articles/<int:article_id>/', views.ArticleProfileView.as_view()),
]
