from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from budget.forms import TransferForm, ExpenditureForm, IncomeForm
from budget.models import Income, Expenditure, Transfer, BankAccount
from budget.services import get_cashflows, get_cashflow_model, get_modelform


class LastOperations(PermissionRequiredMixin, ListView):
    template_name = 'budget/lastoperations.html'
    paginate_by = settings.PAGINATE_BY
    permission_required = ('budget.view_income', 'budget.view_expenditure', 'budget.view_transfer', )

    def get_queryset(self):
        return get_cashflows(
            bank_account_slug=self.request.GET.get('bank_account')
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LastOperations, self).get_context_data(object_list=None, **kwargs)
        context["bank_accounts"] = BankAccount.objects.filter(is_active=True)
        context["current_account"] = BankAccount.objects.get(slug=self.request.GET.get('bank_account')).slug if self.request.GET.get('bank_account') else None
        return context


class CRUDMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.account_slug = self.request.GET.get("bank_account")
        if self.account_slug:
            bank_account = get_object_or_404(BankAccount, slug=self.account_slug)
            kwargs["initial"]['bank_account'] = bank_account
        return kwargs

    def get_success_url(self):
        if self.account_slug:
            return reverse("budget-list") + f"?bank_account={self.account_slug}"
        return reverse_lazy("budget-list")


class IncomeCreate(PermissionRequiredMixin, CRUDMixin, CreateView):
    model = Income
    template_name = "budget/cashflow_edit.html"
    permission_required = "budget.add_income"
    form_class = IncomeForm


class ExpenditureCreate(PermissionRequiredMixin, CRUDMixin, CreateView):
    model = Expenditure
    template_name = "budget/cashflow_edit.html"
    permission_required = "expenditure.add_expenditure"
    form_class = ExpenditureForm


class TransferCreate(PermissionRequiredMixin, CRUDMixin, CreateView):
    model = Transfer
    template_name = "budget/cashflow_edit.html"
    permission_required = "transfer.add_transfer"
    form_class = TransferForm


class EditCashFlow(PermissionRequiredMixin, CRUDMixin, UpdateView):
    permission_required = ('budget.change_income', 'budget.change_expenditure', 'budget.change_transfer', )
    template_name = "budget/cashflow_edit.html"

    def get_form_class(self):
        return get_modelform(self.object)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.account_slug = self.request.GET.get("bank_account")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']
        context['current_account'] = self.account_slug
        return context

    def get_queryset(self):
        id = self.kwargs[self.pk_url_kwarg]
        return get_cashflow_model(id).objects.all()


class DeleteCashFlow(PermissionRequiredMixin, CRUDMixin, DeleteView):
    permission_required = ('budget.delete_income', 'budget.delete_expenditure', 'budget.delete_transfer')

    def get_queryset(self):
        id = self.kwargs[self.pk_url_kwarg]
        return get_cashflow_model(id).objects.all()
