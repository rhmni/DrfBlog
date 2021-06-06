from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializer import ArticleSerializer


class ArticleView(APIView):
    serializer_class = ArticleSerializer

    def get(self, request, article_id=None):
        if article_id is not None:
            article = get_object_or_404(Article.published, pk=article_id)
            srz_data = self.serializer_class(instance=article)
        else:
            articles = Article.published.all()
            srz_data = self.serializer_class(instance=articles, many=True)

        return Response(srz_data.data, status=status.HTTP_200_OK)
