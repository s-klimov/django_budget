from django.urls import re_path

from budget.views import LastOperations, EditCashFlow, DeleteCashFlow, IncomeCreate, ExpenditureCreate, TransferCreate

urlpatterns = [
    re_path(r"^(?P<account>\d+)?$", LastOperations.as_view(), name="budget-list"),
    re_path(
        r"^(?P<account>\d+)?(/)?cashflow/edit/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
        EditCashFlow.as_view(),
        name="cashflow-edit"
    ),
    re_path(
        r"^(?P<account>\d+)?(/)?cashflow/delete/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
        DeleteCashFlow.as_view(),
        name="cashflow-delete"
    ),
    re_path(r"^(?P<account>\d+)?(/)?cashflow/create/income$", IncomeCreate.as_view(), name="income-create"),
    re_path(r"^(?P<account>\d+)?(/)?cashflow/create/expenditure$", ExpenditureCreate.as_view(), name="expenditure-create"),
    re_path(r"^(?P<account>\d+)?(/)?cashflow/create/transfer$", TransferCreate.as_view(), name="transfer-create"),
]
