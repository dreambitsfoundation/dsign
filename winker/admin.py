from django.contrib import admin
from .models import Org, Signatures, User, PrivacySetup
# Register your models here.
admin.site.register(Org)
admin.site.register(User)
admin.site.register(Signatures)
admin.site.register(PrivacySetup)