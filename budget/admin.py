from django.contrib import admin

from budget.models import (
    BankAccount,
    Expenditure,
    Income
)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["name", "incoming_balance"]
    list_filter = ["name"]


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ["value", "bank_account", "category"]
    list_per_page = 10


@admin.register(Income)
class IncomeAdmin(ExpenditureAdmin):
    pass
