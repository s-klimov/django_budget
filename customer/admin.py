from django.contrib import admin
from customer.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', ]
    exclude = ("deleted_at", )


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    exclude = ("deleted_at", )
