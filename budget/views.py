from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from budget.services import get_cashflows, get_cashflow_model, get_modelform


class LastOperations(ListView):
    template_name = 'budget/lastoperations_list.html'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        return get_cashflows()


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