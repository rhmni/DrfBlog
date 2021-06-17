from rest_framework import serializers
from app_blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'author',
            'category',
            'title',
            'slug',
            'body',
            'poster',
            'publish_date',
        )


class ArticleProfileSerializer(serializers.ModelSerializer):
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
            'publish_date',
            'status',
        )

        read_only_fields = (
            'author',
            'publish_date',
        )
