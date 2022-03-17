from django.contrib import admin

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


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "incoming_balance", "outcoming_balance")
    exclude = ("deleted_at", )
    list_filter = ("name", )


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ("value", "bank_account", "operation_date", )
    list_editable = ("operation_date", )
    exclude = ("deleted_at", )
    list_per_page = 10


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
