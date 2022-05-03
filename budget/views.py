from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView, CreateView

from budget.models import Income, Expenditure, Transfer, BankAccount
from budget.services import get_cashflows, get_cashflow_model, get_modelform


class LastOperations(ListView):
    template_name = 'budget/lastoperations_list.html'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        return get_cashflows(
            bank_account_id=self.kwargs.get('account')
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LastOperations, self).get_context_data(object_list=None, **kwargs)
        context["bank_accounts"] = BankAccount.objects.filter(is_active=True)
        return context

    @method_decorator(permission_required('budget.view_income'))
    @method_decorator(permission_required('budget.view_expenditure'))
    @method_decorator(permission_required('budget.view_transfer'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class EditCashFlow(DetailView):
    template_name = "budget/cashflow_edit.html"

    def get_queryset(self):
        id = self.kwargs[self.pk_url_kwarg]
        return get_cashflow_model(id).objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = get_modelform(self.object)(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = get_modelform(instance)(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("budget-list"))
        else:
            messages.error(request, form.errors)

    @method_decorator(permission_required('budget.change_income'))
    @method_decorator(permission_required('budget.change_expenditure'))
    @method_decorator(permission_required('budget.change_transfer'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeleteCashFlow(DeleteView):
    success_url = reverse_lazy("budget-list")

    def get_queryset(self):
        id = self.kwargs[self.pk_url_kwarg]
        return get_cashflow_model(id).objects.all()

    @method_decorator(permission_required('budget.delete_income'))
    @method_decorator(permission_required('budget.delete_expenditure'))
    @method_decorator(permission_required('budget.delete_transfer'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class IncomeCreate(PermissionRequiredMixin, CreateView):
    model = Income
    fields = ["bank_account", "operation_date", "value", "sub_category"]
    template_name = "budget/cashflow_edit.html"
    success_url = reverse_lazy("budget-list")
    permission_required = "budget.add_income"


class ExpenditureCreate(PermissionRequiredMixin, CreateView):
    model = Expenditure
    fields = ["bank_account", "operation_date", "value", "sub_category"]
    template_name = "budget/cashflow_edit.html"
    success_url = reverse_lazy("budget-list")
    permission_required = "expenditure.add_expenditure"


class TransferCreate(PermissionRequiredMixin, CreateView):
    model = Transfer
    fields = ["bank_account", "operation_date", "value", "bank_account_to"]
    template_name = "budget/cashflow_edit.html"
    success_url = reverse_lazy("budget-list")
    permission_required = "transfer.add_transfer"
