from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app_comment.models import Comment
from app_comment.serializers import CommentSerializer, SubCommentSerializer


class CommentListView(APIView):
    def get(self, request):
        comments = Comment.objects.filter(is_confirm=True, is_delete=False, is_sub=False)
        srz_data = CommentSerializer(instance=comments, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class SubCommentListView(APIView):
    def get(self, request):
        comments = Comment.objects.filter(is_confirm=True, is_delete=False, is_sub=True)
        srz_data = SubCommentSerializer(instance=comments, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)
