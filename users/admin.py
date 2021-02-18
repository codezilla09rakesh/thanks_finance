from django.contrib import admin
from users.models import User,Transaction,Subscriptions,Plan, BookMark
from users.form import CustomUserForm
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin

from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken
from cities_light.models import City, SubRegion

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name')
    exclude = ('groups', 'last_login', 'user_permissions', 'password', 'role')
    empty_value_display = 'unknown'
    list_filter = ('is_active', 'is_superuser', 'created_at')
    search_fields = ['username', 'first_name', 'last_name']



admin.site.site_header = 'THANKS FINANCE'
admin.site.site_title = 'THANKS FINANCE'
admin.site.index_title = "THANKS FINANCE"

admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
admin.site.register(Plan)
admin.site.register(Transaction)
admin.site.register(Subscriptions)
admin.site.register(BookMark)

# Read this url to understand this admin.autodiscover()
# https://stackoverflow.com/questions/29502725/unregistering-a-third-party-modeladmin-in-django-causes-notregistered-error

admin.autodiscover()
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(RefreshToken)
admin.site.unregister(Grant)

admin.site.unregister(City)
admin.site.unregister(SubRegion)
# admin.site.empty_value_display = 'None'
