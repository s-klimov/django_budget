from uuid import UUID

from django import forms
from django.db.models import Value, CharField, F
from django.http import Http404
from django.shortcuts import get_object_or_404

from budget.forms import IncomeForm, ExpenditureForm, TransferForm
from budget.models import Income, Expenditure, Transfer, BankAccount
from timestamps.models import Model


def get_cashflows(bank_account_id=None):
    bank_account = get_object_or_404(BankAccount, id=bank_account_id) if bank_account_id else None
    manager = Income.objects.all() if not bank_account else Income.objects.filter(bank_account=bank_account)
    incomes = manager.annotate(
        kind=Value("+", output_field=CharField())
    ).annotate(
        comment=F("sub_category__name")
    )

    manager = Expenditure.objects.all() if not bank_account else Expenditure.objects.filter(bank_account=bank_account)
    expenditures = manager.annotate(
        kind=Value("-", output_field=CharField())
    ).annotate(
        comment=F("sub_category__name")
    )

    manager = Transfer.objects.all() if not bank_account else Transfer.objects.filter(bank_account=bank_account)
    transfers = manager.annotate(
        kind=Value("->", output_field=CharField())
    ).annotate(
        comment=F("bank_account_to__name")
    )
    return incomes.union(transfers.union(expenditures)).order_by(
        "-operation_date", "-kind", "bank_account", "value"
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
