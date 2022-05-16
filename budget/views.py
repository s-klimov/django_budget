from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from django.core.exceptions import ObjectDoesNotExist

from budget.forms import TransferForm, ExpenditureForm, IncomeForm
from budget.models import Income, Expenditure, Transfer, BankAccount, IncomeSubCategory, ExpenditureSubCategory
from budget.services import get_cashflows, get_cashflow_model, get_modelform


class LastOperations(ListView):
    template_name = 'budget/lastoperations.html'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        return get_cashflows(
            bank_account_slug=self.kwargs.get('account'),
            profile=self.request.user.profile
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LastOperations, self).get_context_data(object_list=None, **kwargs)
        context["bank_accounts"] = BankAccount.objects.filter(is_active=True, profile=self.request.user.profile)
        context["current_account"] = BankAccount.objects.get(slug=self.kwargs['account'],
                                                             profile=self.request.user.profile).slug \
            if self.kwargs.get('account') else None
        return context

    @method_decorator(permission_required('budget.view_income'))
    @method_decorator(permission_required('budget.view_expenditure'))
    @method_decorator(permission_required('budget.view_transfer'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LastOperationsHousehold(ListView):
    template_name = 'budget/lastoperations_household.html'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        try:
            household = self.request.user.household
        except ObjectDoesNotExist:
            household = self.request.user.profile.household.first()

        return get_cashflows(
            bank_account_slug=self.kwargs.get('account'),
            profile=self.request.user.profile,
            household=household
        )

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(LastOperationsHousehold, self).get_context_data(object_list=None, **kwargs)
    #     context["bank_accounts"] = BankAccount.objects.filter(is_active=True, profile=self.request.user.profile)
    #     context["current_account"] = BankAccount.objects.get(slug=self.kwargs['account'],
    #                                                          profile=self.request.user.profile).slug \
    #         if self.kwargs.get('account') else None
    #     return context

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

    def form_fields_filter(self, form):
        form.fields['bank_account'].queryset = BankAccount.objects.filter(profile=self.request.user.profile)
        form_class_name = type(form).__name__

        match form_class_name:
            case 'TransferForm':
                form.fields['bank_account_to'].queryset = BankAccount.objects.filter(profile=self.request.user.profile)
            case 'IncomeForm':
                form.fields['sub_category'].queryset = IncomeSubCategory.\
                    objects.filter(category__profile=self.request.user.profile)
            case 'ExpenditureForm':
                form.fields['sub_category'].queryset = ExpenditureSubCategory. \
                    objects.filter(category__profile=self.request.user.profile)

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = get_modelform(self.object)(instance=self.object)
        form = self.form_fields_filter(form)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = get_modelform(instance)(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            kwargs = {"account": self.kwargs['account']} if self.kwargs.get('account') else None
            success_url = reverse("budget-list", kwargs=kwargs)
            return HttpResponseRedirect(success_url)
        else:
            messages.error(request, form.errors)

    @method_decorator(permission_required('budget.change_income'))
    @method_decorator(permission_required('budget.change_expenditure'))
    @method_decorator(permission_required('budget.change_transfer'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeleteCashFlow(DeleteView):

    def get_queryset(self):
        id = self.kwargs[self.pk_url_kwarg]
        return get_cashflow_model(id).objects.all()

    @method_decorator(permission_required('budget.delete_income'))
    @method_decorator(permission_required('budget.delete_expenditure'))
    @method_decorator(permission_required('budget.delete_transfer'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.kwargs.get('account'):
            return reverse("budget-list", kwargs={"account": self.kwargs['account']})
        return reverse_lazy("budget-list")


class IncomeCreate(PermissionRequiredMixin, CreateView):
    model = Income
    template_name = "budget/cashflow_edit.html"
    permission_required = "budget.add_income"
    form_class = IncomeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs.get('account'):
            bank_account = get_object_or_404(BankAccount, slug=self.kwargs['account'])
            kwargs["initial"]['bank_account'] = bank_account
        return kwargs

    def get_success_url(self):
        if self.kwargs.get('account'):
            return reverse("budget-list", kwargs={"account": self.kwargs['account']})
        return reverse_lazy("budget-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        form.fields['bank_account'].queryset = BankAccount.objects.filter(profile=self.request.user.profile)
        form.fields['sub_category'].queryset = IncomeSubCategory. \
            objects.filter(category__profile=self.request.user.profile)
        context["form"] = form
        return context


class ExpenditureCreate(PermissionRequiredMixin, CreateView):
    model = Expenditure
    template_name = "budget/cashflow_edit.html"
    permission_required = "expenditure.add_expenditure"
    form_class = ExpenditureForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs.get('account'):
            bank_account = get_object_or_404(BankAccount, slug=self.kwargs['account'])
            kwargs["initial"]['bank_account'] = bank_account
        return kwargs

    def get_success_url(self):
        if self.kwargs.get('account'):
            return reverse("budget-list", kwargs={"account": self.kwargs['account']})
        return reverse_lazy("budget-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        form.fields['bank_account'].queryset = BankAccount.objects.filter(profile=self.request.user.profile)
        form.fields['sub_category'].queryset = ExpenditureSubCategory. \
            objects.filter(category__profile=self.request.user.profile)
        context["form"] = form
        return context


class TransferCreate(PermissionRequiredMixin, CreateView):
    model = Transfer
    template_name = "budget/cashflow_edit.html"
    permission_required = "transfer.add_transfer"
    form_class = TransferForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs.get('account'):
            bank_account = get_object_or_404(BankAccount, slug=self.kwargs['account'])
            kwargs["initial"]['bank_account'] = bank_account
        return kwargs

    def get_success_url(self):
        if self.kwargs.get('account'):
            return reverse("budget-list", kwargs={"account": self.kwargs['account']})
        return reverse_lazy("budget-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        form.fields['bank_account'].queryset = BankAccount.objects.filter(profile=self.request.user.profile)
        form.fields['bank_account_to'].queryset = BankAccount.objects.filter(profile=self.request.user.profile)
        context["form"] = form
        return context
