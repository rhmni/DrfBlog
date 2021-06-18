import random
from datetime import datetime
from kavenegar import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import redis
from app_account.models import User
from app_account.serializer import (
    ChangePassworSerializer,
    UserRegisterSerializer,
    PhoneSerializer,
    PhoneVerificationSerializer,
)


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


class SendSmsView(APIView):
    serializer_class = PhoneSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            phone_number = srz_data.validated_data['phone']
            print(srz_data.validated_data)
            r = redis.StrictRedis()
            otp_code = random.randint(100000, 999999)
            r.set(phone_number, otp_code)

            # time is seconds
            r.expire(phone_number, 120)
            api = KavenegarAPI(
                '4C45754C704E78554D4E5A42535A68595254474D5339627056495A35334D7738794447467A2B574D5177453D'
            )
            params = {
                'sender': '1000596446',
                'receptor': phone_number,
                'message': f'your code is {otp_code} , time is 120 seconds',
            }
            response = api.sms_send(params)
            return Response({'message': 'code send successfully!'})


class VerificationPhoneView(APIView):
    serializer_class = PhoneVerificationSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            data = srz_data.validated_data

            try:
                User.objects.get(phone=data['phone'])
                return Response({'message': 'this phone is already exists!'})

            except User.DoesNotExist:
                r = redis.StrictRedis()
                if r.exists(data['phone']):
                    otp_code = int(r.get(data['phone']))
                    if otp_code == int(data['otp_code']):
                        request.user.phone = data['phone']
                        request.user.is_phone_Confirm = True
                        request.user.save()
                        return Response({'message': 'your phone verification successfully'})
                    else:
                        return Response({'message': 'your otp code is wrong'})
                else:
                    return Response({'message': 'your phone is wrong'})
