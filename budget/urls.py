from django.urls import path

from budget.views import LastOperations, EditCashFlow, DeleteCashFlow

urlpatterns = [
    path("", LastOperations.as_view(), name="budget-list"),
    path("cashflow/edit/<uuid:pk>", EditCashFlow.as_view(), name="cashflow-edit"),
    path("cashflow/delete/<uuid:pk>", DeleteCashFlow.as_view(), name="cashflow-delete")
]