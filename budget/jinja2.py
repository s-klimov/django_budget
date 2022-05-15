from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

from budget.models import BankAccount


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'accounts_list': BankAccount.objects.filter(is_active=True).order_by("-created_at"),
    })
    return env
