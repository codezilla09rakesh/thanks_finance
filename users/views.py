import uuid
from django.shortcuts import render
from django.http import HttpResponse
from users.serializers import RegistrationSerializer, ResetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from time import time
from datetime import datetime, timedelta,timezone

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
class ResetPassword(APIView):
    def post(self, request, *args, **kwargs):
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
        try:
            token = request.GET['token']
            print('token',token)
            user = User.objects.get(reset_token=token)
            return Response(data={'User': user.first_name,'token':token})
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})

class ChangePassword(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token = request.GET['token']
            user = User.objects.get(reset_token=token)
            now = datetime.now(timezone.utc)
            current = User.objects.get(username='admin')
            diff = now - current.modified_at
            mins = diff.seconds//60
            if mins > 15:
                return Response(data={"time":"Link has expire"}, status=status.HTTP_304_NOT_MODIFIED)
            else:
                password=request.data['password']
                user.set_password(password)
                token  = uuid.uuid4()
                user.reset_token = token
                user.save()  

            return Response(data={'success': "Password Successfully Change"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"message":str(e)}, status=status.HTTP_304_NOT_MODIFIED)

