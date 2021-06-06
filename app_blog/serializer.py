from rest_framework import serializers

from app_blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id',
            'author',
            'category',
            'title',
            'slug',
            'body',
            'poster',
        )
