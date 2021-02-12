from django import forms
from rest_framework import serializers
from users.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


