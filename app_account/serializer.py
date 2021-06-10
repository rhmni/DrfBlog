from rest_framework import serializers
from app_blog.models import Article


class ChangePassworSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50, min_length=8)

    def validate_new_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password


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
