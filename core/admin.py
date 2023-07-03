from django.contrib import admin
from core.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', "birthdate"]
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    fields = ['username', 'first_name', 'last_name', 'birthdate', 'email',
              'is_active', 'is_staff', 'date_joined', 'last_login', 'image']


admin.site.register(User, UserAdmin)