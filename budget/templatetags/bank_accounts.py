from django import template

from budget.models import BankAccount

register = template.Library()

@register.inclusion_tag('budget/accounts.html')
def tag_accounts_list():
	return {
		'accounts_list': BankAccount.objects.filter(is_active=True).order_by("-created_at"),
	}