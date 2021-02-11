import uuid
from datetime import date
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_("Modified At"))
    class Meta:
        abstract = True
class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError("The username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, username, password, **extra_fields):
        # print("#####################",extra_fields)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, password, **extra_fields)


class Country(BaseModel):
    country = models.CharField(max_length=150, null=True, blank=True, verbose_name="City")

    def __str__(self):
        return self.country.capitalize()
    
    class Meta:
        verbose_name_plural = "Countries"

class State(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.CharField(max_length=150, null=True, blank=True, verbose_name="City")

    def __str__(self):
        return self.state.capitalize()
    
    class Meta:
        verbose_name_plural = "States"


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_OPTIONS = (
        ("Male", _("Male")),
        ("Female", _("Female")),
        ("Other", _("Other"))
    )

    SUBSCRIPTION_STATUS = (
        ('Subscribed', _('Subscribed')),
        ('Not Subscribed', _('Not Subscribed')),
    )
    VISIT_REASON = (
        ('Trader', _("I am a Trader.")),
        ('Financial Advisor', _("I'm Financial Advisor.")),
        ('Curious', _("I'm Curious.")),
        ('Other', _("Other Reason.")),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Name"))
    last_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Surname")
    gender = models.CharField(max_length=200, null=True, blank=True, verbose_name="Gender", choices=GENDER_OPTIONS)
    bod = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name="Country", null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, verbose_name="State", null=True, blank=True)
    strip_id = models.CharField(max_length=255, null=True, blank=True)
    visit_reason = models.CharField(max_length=250, choices=VISIT_REASON, null=True, blank=True, verbose_name="Visit Reason")
    profil_pic = models.ImageField(upload_to="profile_pic/", null=True, blank=True, help_text=_("User profile picture"))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_("Modified At"))

    is_active = models.BooleanField(default=False,verbose_name="Active", help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts."
        ))
    # is_superuser = models.BooleanField(default=False,verbose_name="Super User")
    is_staff = models.BooleanField(default=False,verbose_name="Staff",help_text=_("Designates whether this user should be treated as staff."))

    # User to login into account.
    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        # managed = True
        # verbose_name = 'ModelName'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
        # return str(self.first_name)+" "+str(self.last_name)
    

    def fullname(self):
        return self.first_name + " " + self.last_name

class Plan(BaseModel):
    name = models.CharField(max_length=225, null=True, blank=True, verbose_name="Plan Name")
    amount = models.PositiveIntegerField(null=True, blank=True, verbose_name="Plan Price")
    description = models.TextField(null=True, blank=True, verbose_name=_("Plan Description"))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Plans'
    

class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=225, null=True, blank=True) 
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE) 
    transaction_id = models.CharField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        verbose_name_plural = "Transactions"

    
class Subscriptions(BaseModel):
    SUBSCRIPTION_STATUS = (
        ('Current', _('Current')),
        ('Canceled', _('Canceled')),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name="Plan")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, verbose_name="Transaction")
    status = models.CharField(max_length=100, choices=SUBSCRIPTION_STATUS, default="Current")
    valid_till = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.fullname() + "'s: " + self.plan.name + " Plan"






