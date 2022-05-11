from uuid import UUID

from django import forms
from django.db.models import Value, CharField, F
from django.http import Http404
from django.shortcuts import get_object_or_404

from budget.forms import IncomeForm, ExpenditureForm, TransferForm
from budget.models import Income, Expenditure, Transfer, BankAccount
from timestamps.models import Model


def get_cashflows(profile, bank_account_slug=None):
    bank_account = get_object_or_404(BankAccount, slug=bank_account_slug) if bank_account_slug else None
    manager = Income.objects.filter(sub_category__category__profile=profile) if not bank_account \
        else Income.objects.filter(bank_account=bank_account)
    incomes = manager.annotate(
        comment=F("sub_category__name"),
        signed_value=F("value"),
        account=F("bank_account__name"),
    )

    manager = Expenditure.objects.filter(sub_category__category__profile=profile) if not bank_account else Expenditure.objects.filter(bank_account=bank_account)
    expenditures = manager.annotate(
        comment=F("sub_category__name"),
        signed_value=-1 * F("value"),
        account=F("bank_account__name"),
    )

    manager = Transfer.objects.filter(bank_account=bank_account)
    transfers_from = manager.annotate(
        comment=F("bank_account_to__name"),
        signed_value=-1 * F("value"),
        account=F("bank_account__name"),
    )

    # manager = Transfer.objects.all() if not bank_account else Transfer.objects.filter(bank_account_to=bank_account)
    manager = Transfer.objects.filter(bank_account_to=bank_account)
    transfers_to = manager.annotate(
        comment=F("bank_account__name"),
        signed_value=F("value"),
        account=F("bank_account_to__name"),
    )

    return incomes.union(
        expenditures.union(
            transfers_from.union(
                transfers_to
            )
        )
    ).order_by(
        "-operation_date", "bank_account", "-value"
    )


def get_cashflow_model(id: UUID) -> Model:
    try:
        Income.objects.get(id=id)
    except Income.DoesNotExist:
        try:
            Expenditure.objects.get(id=id)
        except Expenditure.DoesNotExist:
            try:
                Transfer.objects.get(id=id)
            except Transfer.DoesNotExist:
                raise Http404
            else:
                return Transfer
        else:
            return Expenditure
    else:
        return Income


def get_modelform(object: Model) -> forms.ModelForm:
    form: forms.ModelForm
    if isinstance(object, Income):
        form = IncomeForm
    elif isinstance(object, Expenditure):
        form = ExpenditureForm
    else:
        form = TransferForm
    return form
