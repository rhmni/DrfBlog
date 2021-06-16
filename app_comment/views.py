from datetime import datetime
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app_comment.models import Comment
from app_comment.serializers import CommentSerializer, SubCommentSerializer, CreateCommentSerializer


class CommentListView(APIView):
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.filter(is_confirm=True, is_delete=False, is_sub=False)
        srz_data = self.serializer_class(instance=comments, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class SubCommentListView(APIView):
    serializer_class = SubCommentSerializer

    def get(self, request, comment_id):
        comments = Comment.objects.filter(is_confirm=True, is_delete=False, is_sub=True, sub_comment__id=comment_id)
        srz_data = self.serializer_class(instance=comments, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class CreateCommentView(APIView):
    serializer_class = CreateCommentSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save(
                writer=request.user,
                register_date=datetime.now(),
            )
            return Response(srz_data.data, status=status.HTTP_201_CREATED)


class DeleteCommentView(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, is_delete=False, is_confirm=True, writer=request.user)
        comment.is_delete = True
        comment.save()
        return Response({'message': 'comment deleted successfully!'})
