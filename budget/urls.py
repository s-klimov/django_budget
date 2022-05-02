from django.urls import path

from budget.views import LastOperations, EditCashFlow

urlpatterns = [
    path("", LastOperations.as_view(), name="budget-list"),
    path("cashflow/<uuid:pk>", EditCashFlow.as_view(), name="budget-edit")
]