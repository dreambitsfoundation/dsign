from django import forms
from .models import Org, Signatures, User

class OrgUserRegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['org','username','email','password','designation','phone','pan']

class PersonalUserRegistration(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','email','password','phone','pan']

class OrgRegistration(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=Org
        fields=["name","address","contact_mail","password","phone","website","pan"]

class ProUserUpdate(forms.ModelForm):
    #password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=["email","designation","phone","dob","address","gender"]

class UserUpdate(forms.ModelForm):

    class Meta:
        model=User
        fields=["email","phone","dob","address","gender"]




