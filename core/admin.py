from django.contrib import admin
from core.models import User
from goals.models import GoalCategory


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', "birthdate"]
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    fields = ['username', 'first_name', 'last_name', 'birthdate', 'email',
              'is_active', 'is_staff', 'date_joined', 'last_login', 'image']


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user__username")


admin.site.register(User, UserAdmin)
admin.site.register(GoalCategory, GoalCategoryAdmin)

