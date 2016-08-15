from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.core import validators
import re

# Create your models here.
class Org(models.Model):
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    website=models.CharField(max_length=50,default="NULL")
    contact_mail=models.EmailField()
    active=models.BooleanField(default=True)
    created=models.DateTimeField(default="2015-01-01 12:00:00.0000")
    pan=models.CharField(max_length=15)
    admin=models.CharField(max_length=100)
    phone=models.CharField(max_length=10,)
    password=models.CharField(max_length=100,)
    latest_signature_purchase=models.IntegerField(default=0)
    total_signature_purchased=models.IntegerField(default=0)
    signatures_left=models.IntegerField(default=0)
    signatures_used=models.IntegerField(default=0)
    show_phone=models.BooleanField(default=True)
    show_website=models.BooleanField(default=True)
    show_address=models.BooleanField(default=True)
    show_eco_savings=models.BooleanField(default=True)
    show_staff_mail=models.BooleanField(default=True)
    show_staff_phone=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class User(AbstractBaseUser,PermissionsMixin):
    org=models.ForeignKey(Org,on_delete=models.CASCADE, default=0)
    username=models.CharField(max_length=100)
    code=models.TextField(default="NULL")
    email=models.EmailField(unique=True)
    org_mail=models.EmailField(default="NULL")
    #password=models.CharField(max_length=200)
    designation=models.CharField(max_length=50,)
    is_active=models.BooleanField(default=True)
    date_created=models.DateTimeField(default="NULL",blank=True)
    is_admin=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_valid=models.BooleanField(default=False)
    signature_provided_org=models.IntegerField(default=0)
    signature_left_org=models.IntegerField(default=0)
    signature_provided_per=models.IntegerField(default=3)
    signature_left_per=models.IntegerField(default=3)
    pan=models.CharField(max_length=10,)
    phone=models.CharField(max_length=10)
    is_staff = models.BooleanField(default=True)
    has_org=models.BooleanField(default=False)
    address=models.TextField(default="NULL")
    gender=models.CharField(max_length=1, default="NULL")
    dob=models.CharField(default="NULL",blank=True,max_length=10)
    date_org_created=models.CharField(default="NULL", max_length=30)

    objects=UserManager()

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD= 'email'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.email

class Signatures(models.Model):
    code=models.CharField(max_length=100)
    header=models.CharField(max_length=100)
    org=models.ForeignKey(Org,on_delete=models.CASCADE, default=0)
    addressed_to=models.CharField(max_length=100)
    created=models.CharField(max_length=100, default="NULL")
    subject=models.TextField(default="NULL",blank=True)
    signatory=models.CharField(max_length=500)
    contact=models.CharField(max_length=500)
    is_flagged=models.BooleanField(default=False)
    flagged_on=models.DateTimeField(default=timezone.now)
    flag_reason=models.TextField(default='NULL')
    flagged_by=models.TextField(default="NULL")
    comments=models.TextField(default="NULL", blank=True)
    date_created=models.DateTimeField(default=timezone.now)
    is_valid=models.BooleanField(default=True)
    invalidated_by=models.CharField(default="NULL",max_length=200,blank=True)
    invalidated_on=models.DateTimeField(default=timezone.now)
    invalidated_reason=models.TextField(default="NULL",blank=True)
    is_haulted=models.BooleanField(default=False)
    hault_user_permission=models.BooleanField(default=False)


    def __str__(self):
        return self.code

class PrivacySetup(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    personal_result_phone_number=models.BooleanField(default=True)
    professional_result_phone_number=models.BooleanField(default=True)
    profile_view_phone_number=models.BooleanField(default=True)
    personal_result_email=models.BooleanField(default=True)
    professional_result_email=models.BooleanField(default=True)
    profile_view_email=models.BooleanField(default=True)
    personal_result_address=models.BooleanField(default=True)
    professional_result_address=models.BooleanField(default=True)
    profile_view_address=models.BooleanField(default=True)
    personal_result_gender=models.BooleanField(default=False)
    profile_view_gender=models.BooleanField(default=True)
    show_dob=models.BooleanField(default=False)

    def __str__(self):
        return self.user

class Notification(models.Model):
    type=models.CharField(max_length=10,default="NULL")
    date_created=models.DateTimeField(default=timezone.now)
    created_by=models.TextField(default="NULL")
    targeted_audience=models.TextField(default="NULL")
    seen=models.BooleanField(default=False)
    seen_on=models.DateTimeField(default=timezone.now)
    request_user=models.TextField(default="NULL")
    request_signature=models.TextField(default="NULL")
    request_operation=models.TextField(default="NULL")
    org_related=models.ForeignKey(Org, on_delete=models.CASCADE, default=0)
    code=models.TextField(default="NULL")
    request_denied=models.BooleanField(default=False)

    def __str__(self):
        return self.code

class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=0)
    org=models.ForeignKey(Org, on_delete=models.CASCADE, default=0)
    date_of_purchase=models.DateTimeField(default=timezone.now)
    amount=models.IntegerField(default=0)
    total_payment=models.IntegerField(default=0)
    code=models.TextField(default="NULL")

    def __str__(self):
        return self.code