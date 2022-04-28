from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated

from budget.models import (
    BankAccount,
    Expenditure,
    Income,
    ExpenditureCategory,
    ExpenditureSubCategory,
    IncomeCategory,
    IncomeSubCategory,
    Transfer,
)


class IncomeInline(TabularInlinePaginated):
    model = Income
    fields = ("operation_date", "sub_category", "value", "bank_account", )
    extra = 0
    ordering = ("-operation_date", "bank_account", )
    classes = ('collapse',)
    per_page = 5


class ExpenditureInline(IncomeInline):
    model = Expenditure
    per_page = 10


class TransferInline(IncomeInline):
    model = Transfer
    fields = ("operation_date", "bank_account", "value", "bank_account_to", )
    fk_name = "bank_account"
    per_page = 8


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "incoming_balance", "outcoming_balance")
    exclude = ("deleted_at", )
    list_filter = ("name", )
    save_on_top = True

    inlines = [
        ExpenditureInline,
        TransferInline,
        IncomeInline,
    ]


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ("value", "bank_account", "operation_date", )
    list_editable = ("operation_date", )
    exclude = ("deleted_at", )
    list_per_page = 20


@admin.register(Income)
class IncomeAdmin(ExpenditureAdmin):
    pass


class ExpenditureSubCategoryTabularInLine(admin.TabularInline):
    model = ExpenditureSubCategory
    exclude = ("deleted_at", )
    extra = 0


class IncomeSubCategoryTabularInLine(ExpenditureSubCategoryTabularInLine):
    model = IncomeSubCategory


@admin.register(ExpenditureCategory)
class ExpenditureCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    exclude = ("deleted_at", )
    list_filter = ("name", )
    inlines = (ExpenditureSubCategoryTabularInLine, )


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(ExpenditureCategoryAdmin):
    inlines = (IncomeSubCategoryTabularInLine,)


@admin.register(Transfer)
class TransferAdmin(ExpenditureAdmin):
    list_display = ("value", "bank_account",  "bank_account_to", "operation_date", )
