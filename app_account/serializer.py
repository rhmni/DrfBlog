from rest_framework import serializers

from app_account.models import User


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    name = serializers.CharField(max_length=150)
    password_1 = serializers.CharField(max_length=50, min_length=8)
    password_2 = serializers.CharField(max_length=50, min_length=8)

    def validate(self, validated_data):
        try:

            User.objects.get(username=validated_data['username'])
            raise serializers.ValidationError('this username is already exist.')

        except User.DoesNotExist:

            if validated_data['password_1'] != validated_data['password_2']:
                raise serializers.ValidationError('passwords not match.')
            if not any(char.isdigit() for char in validated_data['password_2']):
                raise serializers.ValidationError('Password must contain digit.')
            if not any(char.isalpha() for char in validated_data['password_2']):
                raise serializers.ValidationError('Password must contain alpha.')

        return validated_data


class ChangePassworSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50, min_length=8)

    def validate_new_password(self, password):
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain digit.')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain alpha.')
        return password


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):

        if len(value) != 11:
            raise serializers.ValidationError('phone must be 11 character')
        if not value.isnumeric():
            raise serializers.ValidationError('phone must be only number')
        if not value.startswith('09'):
            raise serializers.ValidationError('phone must start with "09"')
        return value


class PhoneVerificationSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp_code = serializers.CharField()

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError('phone must be 11 character')
        if not value.isnumeric():
            raise serializers.ValidationError('phone must be only number')
        if not value.startswith('09'):
            raise serializers.ValidationError('phone must start with "09"')
        return value

    def validate_otp_code(self, value):
        if len(value) != 6:
            raise serializers.ValidationError('otp code must be 6 character')
        if not value.isnumeric():
            raise serializers.ValidationError('otp code must be only number')

        return value
