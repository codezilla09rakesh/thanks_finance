from django.urls import path
from users import views

urlpatterns=[
    path('reset_password/', views.ResetPassword.as_view(), name="reset_password"),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    ]