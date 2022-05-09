

from rest_framework import serializers
from .models import Global, RegisterUsers, Spam
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.modelfields import PhoneNumberField

class RegisterUsersSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(
    validators=[UniqueValidator(queryset=RegisterUsers.objects.all())]
  )
    password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = RegisterUsers
        fields = '__all__'

      
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUsers
        fields = '__all__'


class SpamSerializer(serializers.ModelSerializer):
  PhoneNumberField(
    validators=[UniqueValidator(queryset=Spam.objects.all())]
  )
  class Meta:
        model = Spam
        fields = ['phone']

class  GlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Global
        fields = '__all__'


