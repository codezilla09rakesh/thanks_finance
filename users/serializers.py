from rest_framework import serializers
from users.models import User, Plan, Transaction, Subscriptions
from cities_light.models import Country, Region

class ResetSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=225)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields =['id', 'name']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'country']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'gender', 'bod', 'country', 'state', 'profile_pic', 'visit_reason']

    # def create(self, validated_data):
    #     user = super(RegistrationSerializer, self).create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True, write_only=True, allow_null=False)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'}, allow_null=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bod', 'country', 'state', 'profile_pic']

class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"

class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = "__all__"

class UpdateSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ['plan', 'transaction', 'status', 'valid_till']