from datetime import datetime
from rest_framework import status
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
