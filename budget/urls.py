from django.urls import path, re_path

from budget.views import LastOperations, EditCashFlow, DeleteCashFlow, IncomeCreate, ExpenditureCreate, TransferCreate

urlpatterns = [
    re_path(r"^(?P<account>\d+)?$", LastOperations.as_view(), name="budget-list"),
    path("cashflow/edit/<uuid:pk>", EditCashFlow.as_view(), name="cashflow-edit"),
    path("cashflow/delete/<uuid:pk>", DeleteCashFlow.as_view(), name="cashflow-delete"),
    path("cashflow/create/income", IncomeCreate.as_view(), name="income-create"),
    path("cashflow/create/expenditure", ExpenditureCreate.as_view(), name="expenditure-create"),
    path("cashflow/create/transfer", TransferCreate.as_view(), name="transfer-create"),
]
