from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'phone', 'city', 'gender', 'is_active')
    list_filter = ('city', 'is_active')
    fieldsets = (
        ('User Details', {
         'fields': ('first_name', 'last_name', 'email', 'phone', 'city', 'gender', 'profile_img',)}),
        ('Permissions', {'fields': ('user_type', 'is_staff',
         'is_active', 'user_permissions',)}),
        ('Dates', {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        ('User Details', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'user_permissions')}
         ),
    )
    search_fields = ('email', 'phone')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
