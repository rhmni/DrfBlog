from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app_account.forms import UserChangeForm, UserCreationForm
from app_account.models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'id', 'name', 'email', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        ('Security information', {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'bio', 'avatar', 'phone')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_phone_Confirm')}),
        ('Important date', {'fields': ('date_of_birth', 'last_login', 'join_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name', 'username', 'bio')
    ordering = ('-id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
