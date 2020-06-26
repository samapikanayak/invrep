from django.contrib import admin
from .models import *
# Register your models here.
class UserSignupAdmin(admin.ModelAdmin):
    list_display = ["fullname","email","phn"]
admin.site.register(UserSignup,UserSignupAdmin)