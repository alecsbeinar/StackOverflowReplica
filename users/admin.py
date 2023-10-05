from django.contrib import admin

from qa.admin import AnswerAdmin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'password']
    inlines = (AnswerAdmin,)

