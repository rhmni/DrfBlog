from rest_framework import serializers
from app_comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'writer',
            'article',
            'body',
            'register_date',
        )


class SubCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'writer',
            'article',
            'sub_comment',
            'body',
            'register_date',
        )


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'writer',
            'article',
            'body',
            'register_date',
        )

        read_only_fields = (
            'writer',
            'register_date',
        )
