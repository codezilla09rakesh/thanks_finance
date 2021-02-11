from django import forms
from users.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"