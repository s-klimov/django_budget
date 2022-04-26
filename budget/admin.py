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
    History,
)


class HistoryInline(admin.TabularInline):
    verbose_name = "операции"
    verbose_name_plural = "история операций"
    model = History
    exclude = ("id", )
    extra = 0
    ordering = ("-operation_date", "bank_account", "type", )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "incoming_balance", "outcoming_balance")
    exclude = ("deleted_at", )
    list_filter = ("name", )
    save_on_top = True

    inlines = [
        HistoryInline,
    ]


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
