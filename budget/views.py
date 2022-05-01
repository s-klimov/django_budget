from django.views.generic import ListView

from budget.models import Income, Expenditure, Transfer


class LastOperations(ListView):
    template_name = 'budget/lastoperations_list.html'
    ordering = ("-operation_date", )
    def get_queryset(self):
        incomes = Income.objects.all()
        expenditures = Expenditure.objects.all()
        transfers = Transfer.objects.all()
        return incomes.union(transfers.union(expenditures))
