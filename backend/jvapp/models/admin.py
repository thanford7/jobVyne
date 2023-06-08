from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from jvapp.models.employer import *
from jvapp.models.job_seeker import *
from jvapp.models.karma import DonationOrganization
from jvapp.models.location import *
from jvapp.models.social import *
from jvapp.models.user import UserEmployerPermissionGroup


class JobVyneUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "employer")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_type_bits",
                    "is_employer_deactivated",
                    "employer_permission_group"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_dt")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("last_name", "first_name")
    

@admin.register(UserEmployerPermissionGroup)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Employer, EmployerJob, EmployerAuthGroup, EmployerPermission, EmployerSize, JobDepartment)
class EmployerAdmin(admin.ModelAdmin):
    pass


@admin.register(JobApplication, JobApplicationTemplate)
class JobSeekerAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialPlatform)
class SocialPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order', 'is_displayed')
    ordering = ('sort_order',)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(Country, State, City, Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(DonationOrganization)
class DonationOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
