from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import GoalStatus, ScrumyGoals, ScrumyHistory
from django.contrib.auth.models import User, Group, Permission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'fullname', 'usertype')

class ScrumUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'first_name', 'last_name', 'password', 'email','username', 'fullname', 'usertype')
        


class ScrumGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalStatus
        fields = ('id', 'status_name')
        
        