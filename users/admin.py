from django.contrib import admin
from users.models import User,Country,State,Transaction,Subscriptions,Plan
from users.form import CustomUserForm
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name')
    exclude = ('groups', 'last_login', 'user_permissions', 'password', 'role')
    empty_value_display = 'unknown'
    list_filter = ('is_active', 'is_superuser', 'created_at')



admin.site.site_header = 'THANKS FINANCE'
admin.site.site_title = 'THANKS FINANCE'
admin.site.index_title = "THANKS FINANCE"
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Country)
admin.site.register(Plan)
admin.site.register(State)
admin.site.register(Transaction)
admin.site.register(Subscriptions)
# admin.site.empty_value_display = 'None'
