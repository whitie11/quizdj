from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import QuizUser

class UserAdmin(admin.ModelAdmin):
    list_display = (
   'id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'bio', 'location', 'role')
    list_editable =('email', 'is_active', 'bio', 'location', 'role' )

# Register your models here.
admin.site.register(QuizUser, UserAdmin)

