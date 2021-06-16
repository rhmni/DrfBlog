from django.urls import path
from app_comment import views

app_name = 'comment'
urlpatterns = [
    path('comments/', views.CommentListView.as_view()),
    path('sub-comments/<int:comment_id>/', views.SubCommentListView.as_view()),
    path('comments/create/', views.CreateCommentView.as_view()),
    path('comments/delete/<int:comment_id>/', views.DeleteCommentView.as_view()),
]
