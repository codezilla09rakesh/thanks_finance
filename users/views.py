import uuid
import requests
import re
from users.models import User, Plan, Subscriptions, Transaction

from datetime import datetime, timezone

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


from users.serializers import RegistrationSerializer, LoginSerializer, PasswordChangeSerializer, UserSerializer, CountrySerializer, StateSerializer, PlanSerializer, TransactionSerializer, SubscriptionsSerializer, UpdateSubscriptionsSerializer
from thanks_finance import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import  GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission, IsAuthenticated


from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from cities_light.models import Region, Country

from datetime import timedelta, date

class SignUp(ModelViewSet):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        params: request => username, password, first_name, last_name, email, gender, bod, country, state, profile_pic, visit_reason
        return : message => Successfully user created
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message":"Successfully created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken, APIView):
    def post(self, request, *args, **kwargs):
        """
        params: request => username, password
        return => access_token, expires_in, token_type, scope
        """
        try:
            # check username is email type or not
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
            if re.search(regex, request.data["username"]):
                user = User.objects.filter(username=request.data["username"])
                if len(user):
                    username = user[0].username
                    if user[0].is_active == False:
                        return Response({
                            "message": "Your account has been suspended, please contact customer care service for more information."})
                else:
                    return Response(data={"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.get(username=request.data["username"])
                username = request.data["username"]
                # isVerified = user.isVerified
                # scope = user.role
                if user.is_active == False:
                    return Response({
                        "message": "Your account has been suspended, please contact customer care service for more information."})
                # elif isVerified == False:
                #     return Response({"message": "Email not verified."})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})
        r = requests.post(settings.URL_TYPE + "/o/token/",
                          data={
                              "grant_type": "password",
                              "username": username,
                              "password": request.data["password"],
                              "client_id": settings.CLIENT_ID,
                              "client_secret": settings.CLIENT_SECRET,
                          },
                          # verify=True
                           )
        if r.status_code == 400:
            json_res = {"message": "Bad request or Invalid credentials"}
            return Response(data=json_res, status=r.status_code)
        else:
            return Response(r.json())

class RefreshToken(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Registers user to the server. Input should be in the format:
        {"refresh_token": "<token>"}

        params: request => refresh_token
        return: token, refresh_token
        """
        r = requests.post(
            settings.URL_TYPE + "/o/token/",
            data={
                "grant_type": "refresh_token",
                "refresh_token": request.data["refresh_token"],
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },
            verify=False,
        )
        if r.status_code == 200:
            return Response(r.json())
        else:
            return Response(r.json(), r.status_code)

class RevokeToken(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Method to revoke tokens.
        {"token": "<token>"}
        params: request => token
        return: message => token revoked
        """
        r = requests.post(
            settings.URL_TYPE + "/o/revoke_token/",
            data={
                "token": request.data["token"],
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },)
        # If it goes well return success message (would be empty otherwise)
        if r.status_code == requests.codes.ok:
            return Response({"message": "token revoked"}, r.status_code)
        # Return the error if it goes badly
        return Response(r.json(), r.status_code)

class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        params: request => old password, new password
        return message => password set
        """
        data = request.data
        user = request.user
        serializer = PasswordChangeSerializer(data=data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response(data={"message":"Wrong old Password"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(data={'status': 'password set'}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPassword(APIView):

    def post(self, request, *args, **kwargs):
        """
        params: request => username
        return: message => Reset your password
        """
        try:
            user = User.objects.get(email = request.data['email'])
            token = uuid.uuid4()
            user.reset_token = token
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Reset Your Password'
            # here we create message in the html form in the we pass user,domain,uid,token
            message = render_to_string('users/email.html', {
                'user': user,
                'domain': current_site.domain,
                'token':token,
            })
            to_email = request.data['email']
            # to_email = form.POST.get('username')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return Response(status=status.HTTP_200_OK, data={'message': "We have sent you an email, please confirm your email address to reset password"})
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})

    
    def get(self, request, *args, **kwargs):
        """
        params: request => token,
        return: user First Name, token
        """
        try:
            token = request.GET['token']
            print('token',token)
            user = User.objects.get(reset_token=token)
            return Response(data={'User': user.first_name,'token':token})
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})

class ChangePassword(APIView):
    def post(self, request, *args, **kwargs):
        """
        params: request => token, password
        return : message => Password Successfully Change
        """
        try:
            token = request.GET['token']
            user = User.objects.get(reset_token=token)
            now = datetime.now(timezone.utc)
            current = User.objects.get(username='admin')
            diff = now - current.modified_at
            mins = diff.seconds//60
            if mins > 15:
                return Response(data={"message":"reset password link has expire"}, status=status.HTTP_304_NOT_MODIFIED)
            else:
                password=request.data['password']
                user.set_password(password)
                token  = uuid.uuid4()
                user.reset_token = token
                user.save()
            return Response(data={'message': "Password Successfully Change"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"message":str(e)}, status=status.HTTP_304_NOT_MODIFIED)

class CountryList(ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        params: id = country_id
        return: id, country name
        """
        country = Country.objects.filter(pk = id)
        if country:
            serializer = CountrySerializer(country, many=True)
            data = serializer.data
        else:
            return Response(data={"massage":"Country could not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        return: list of id and country_name
        """
        all_country = Country.objects.all()
        serializer = CountrySerializer(all_country, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


class StateList(ModelViewSet):
    serializer_class = StateSerializer
    queryset = Country.objects.all()

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        params: id = state_id
        return: id, state_name
        """
        state = Region.objects.filter(pk = id)
        if state:
            serializer = StateSerializer(state, many=True)
            data = serializer.data
        else:
            return Response(data={"massage":"state could not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        return: list of id, state_name, country_id
        """
        all_state = Region.objects.all()
        serializer = CountrySerializer(all_state, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

class CountryAndState(GenericAPIView):

    def get(self, request, country_id=None, state_id=None, *args, **kwargs):
        """
        To get one state
        params: id = country_id
                id = state_id
        return: id, state_name

        To get list of state for particular Country
        params: id = country_id
        return: list of id, state_name
        """
        if state_id and country_id:
            try:
                state = Region.objects.get(id= state_id, country=country_id)
                serialzier = StateSerializer(state)
                data = serialzier.data
                return Response(data=data, status=status.HTTP_200_OK)
            except Exception as e :
                return Response(data={"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif country_id:
            try:
                state_list = Region.objects.filter(country=country_id)
                serializer = StateSerializer(state_list, many=True)
                data = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Profile(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        return :  first_name, last_name, email, gender, bod, country, state, profile_pic, visit_reason
        """
        user = request.user
        try:
            user = User.objects.get(username=user)
            serializer = UserSerializer(user)
            data = serializer.data
            return Response(data = data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        params: request =>  first_name, last_name, email, gender, bod, country, state, profile_pic, visit_reason
        return : message => Profile Update
        """
        user = request.user
        user = User.objects.get(username = user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message":"Profile Update"}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PlansView(ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    def list(self, request, *args, **kwargs):
        """
        return => plan_id, name, description, price
        """
        plan_list = Plan.objects.all()
        serializer = PlanSerializer(plan_list, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        return => plan_id, name, description, price
        """
        if id:
            try:
                plan = Plan.objects.get(id=id)
                serializer = PlanSerializer(plan)
                data = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message":"plan_id is none"})

class SubscriptionsView(ModelViewSet):
    serializer_class = SubscriptionsSerializer
    queryset = Subscriptions.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        return =>list of user_id, plan_id, transaction_id, status, valid_till
        """
        user = request.user
        subscriptions = Subscriptions.objects.filter(user = user)
        serializer = SubscriptionsSerializer(subscriptions, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        return => user_id, plan_id ,transaction_id, status, valid_till
        """
        user = request.user
        if id:
            try:
                subscription = Subscriptions.objects.get(id=id, user=user)
                serializer = SubscriptionsSerializer(subscription)
                data = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={"message":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message":"Subscription is not found"})

    def update(self, request, id=None, *args, **kwargs):
        """
        params: request => plan, transaction, status, valid_till
        return : message => successfully updated
        """
        user = request.user
        if id:
            data = request.data
            try:
                subscription = Subscriptions.objects.get(id=id, user=user)
                serializer = UpdateSubscriptionsSerializer(subscription, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data={"message":"Successfully Updated "})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data={"message":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "Subscription is not found"})


class TransactionView(ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        reutrn => user, stripe_id, plan, transaction_id
        """
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        data  = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        params: request => id
        returns => user, stripe_id, plan, transaction_id
        """
        user = request.user
        if id:
            try:
                transaction = Transaction.objects.get(id=id, user=user)
                serializer = TransactionSerializer(transaction, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={'message': str(e)}, status=status.HTTP_404_NOT_FOUND)




