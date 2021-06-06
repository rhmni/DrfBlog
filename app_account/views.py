from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app_blog.models import Article
from app_blog.serializer import ArticleProfileSerializer


class ArticleProfileView(APIView):
    serializer_class = ArticleProfileSerializer

    def get(self, request, article_id=None):
        if article_id is not None:
            article = get_object_or_404(Article.active, author=request.user, pk=article_id)
            srz_data = self.serializer_class(instance=article)
        else:
            articles = Article.active.filter(author=request.user)
            srz_data = self.serializer_class(instance=articles, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)

