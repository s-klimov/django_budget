from django.contrib import admin

from budget.models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    list_editable = ["name"]
