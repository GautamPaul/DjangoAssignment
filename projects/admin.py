from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Projects, Resource


# Register your models here.


class ResourceAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined',
                    'last_login', 'is_admin')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Projects)
admin.site.register(Resource, ResourceAdmin)
