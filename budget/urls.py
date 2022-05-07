from django.urls import re_path

from budget.views import LastOperations, EditCashFlow, DeleteCashFlow, IncomeCreate, ExpenditureCreate, TransferCreate

urlpatterns = [
    re_path(r"^(?P<account>[0-9a-z_-]+)?$", LastOperations.as_view(), name="budget-list"),
    re_path(
        r"^(?P<account>[0-9a-z_-]+)?/cashflow/edit/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
        EditCashFlow.as_view(),
        name="cashflow-edit"
    ),
    re_path(
        r"^(?P<account>[0-9a-z_-]+)?/cashflow/delete/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
        DeleteCashFlow.as_view(),
        name="cashflow-delete"
    ),
    re_path(r"^(?P<account>[0-9a-z_-]+)?/cashflow/create/income$", IncomeCreate.as_view(), name="income-create"),
    re_path(r"^(?P<account>[0-9a-z_-]+)?/cashflow/create/expenditure$", ExpenditureCreate.as_view(), name="expenditure-create"),
    re_path(r"^(?P<account>[0-9a-z_-]+)?/cashflow/create/transfer$", TransferCreate.as_view(), name="transfer-create"),
]
