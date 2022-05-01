from django.urls import path

from budget.views import LastOperations

urlpatterns = [
    path('', LastOperations.as_view(), name='budget-list'),
]