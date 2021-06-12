from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_account.models import User
from app_account.serializer import ChangePassworSerializer, UserRegisterSerializer


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


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            data = srz_data.validated_data
            user = User.objects.create_user(
                username=data['username'],
                name=data['name'],
                password=data['password_2'],
            )
            user.join_date = datetime.now()
            user.save()
            return Response({'message': 'user create successfully!'}, status=status.HTTP_201_CREATED)
