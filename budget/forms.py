from django import forms

from budget.models import Income, Expenditure, Transfer


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        exclude= ("id", "deleted_at", )
        widgets = {
            'operation_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        exclude = ("id", "deleted_at",)
        widgets = {
            'operation_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        exclude = ("id", "deleted_at",)
        widgets = {
            'operation_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }
