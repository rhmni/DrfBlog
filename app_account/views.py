from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app_account.serializer import ChangePassworSerializer
from app_blog.models import Article
from app_blog.serializer import ArticleProfileSerializer
from permissions import IsOwnerOrReadOnly


class ChangePasswordView(APIView):
    serializer_class = ChangePassworSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        user = request.user
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            data = srz_data.validated_data
            if user.check_password(data['old_password']):
                user.set_password(data['new_password'])
                user.save()
                return Response({'message': 'password changed successfully!'})
            else:
                return Response({'message': 'old password is wrong!'})


class ArticleProfileView(APIView):
    serializer_class = ArticleProfileSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request, article_id=None):
        if article_id is not None:
            article = get_object_or_404(Article.active, author=request.user, pk=article_id)
            srz_data = self.serializer_class(instance=article)
        else:
            articles = Article.active.filter(author=request.user)
            srz_data = self.serializer_class(instance=articles, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class ArticleCreateProfileView(APIView):
    serializer_class = ArticleProfileSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save(
                author=request.user,
            )

            # checking if status that user selected is unconfirmed or published set that, to draft
            if srz_data.validated_data['status'] == 'P' or srz_data.validated_data['status'] == 'U':
                srz_data.save(
                    status='D',
                )
            return Response(srz_data.data, status=status.HTTP_201_CREATED)


class ArticleUpdateProfileView(APIView):
    serializer_class = ArticleProfileSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )

    def patch(self, request, article_id):
        article = get_object_or_404(Article.active, pk=article_id)
        self.check_object_permissions(request, article)

        srz_data = self.serializer_class(instance=article, data=request.data, partial=True)

        if srz_data.is_valid(raise_exception=True):
            srz_data.save()

            # checking if status that user selected is unconfirmed or published set that, to draft
            if srz_data.validated_data['status'] == 'P' or srz_data.validated_data['status'] == 'U':
                srz_data.save(
                    status='D',
                )
            return Response(srz_data.data, status=status.HTTP_204_NO_CONTENT)


class ArticleDeleteProfileView(APIView):
    permission_classes = (
        IsOwnerOrReadOnly,
    )

    def delete(self, request, article_id):
        article = get_object_or_404(Article.active, pk=article_id)
        self.check_object_permissions(request, article)
        article.is_delete = True
        article.save()
        return Response({'message': 'deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
