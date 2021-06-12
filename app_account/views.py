from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app_account.serializer import ChangePassworSerializer


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
