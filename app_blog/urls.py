from django.urls import path
from app_blog import views

app_name = 'blog'
urlpatterns = [
    path('articles/', views.ArticleView.as_view()),
    path('articles/<int:article_id>/', views.ArticleView.as_view()),
    path('articles/category/<slug:slug>/', views.ArticleCategoryView.as_view()),

    # profile articles urls
    path('profile/articles/', views.ArticleProfileView.as_view()),
    path('profile/articles/<int:article_id>/', views.ArticleProfileView.as_view()),
    path('profile/articles/create/', views.ArticleCreateProfileView.as_view()),
    path('profile/articles/delete/<int:article_id>/', views.ArticleDeleteProfileView.as_view()),
    path('profile/articles/update/<int:article_id>/', views.ArticleUpdateProfileView.as_view()),
]
