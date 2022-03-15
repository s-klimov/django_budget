from django.contrib import admin

from budget.models import (
    BankAccount,
    Expenditure,
    Income,
)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "incoming_balance", "outcoming_balance")
    exclude = ("deleted_at", )
    list_filter = ("name", )


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ("value", "bank_account", "tag_list", )
    exclude = ("deleted_at", )
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(Income)
class IncomeAdmin(ExpenditureAdmin):
    pass

