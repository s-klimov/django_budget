from django.conf import settings
from django.db.models import Value, CharField, F
from django.views.generic import ListView

from budget.models import Income, Expenditure, Transfer


class LastOperations(ListView):
    template_name = 'budget/lastoperations_list.html'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        incomes = Income.objects.all().annotate(
            kind=Value("+",output_field=CharField())
        ).annotate(
            comment=F("sub_category__name")
        )
        expenditures = Expenditure.objects.all().annotate(
            kind=Value("-", output_field=CharField())
        ).annotate(
            comment=F("sub_category__name")
        )
        transfers = Transfer.objects.all().annotate(
            kind=Value("->", output_field=CharField())
        ).annotate(
            comment=F("bank_account_to__name")
        )
        return incomes.union(transfers.union(expenditures)).order_by(
            "-operation_date", "-kind", "bank_account", "value"
        )
