from django import template

from budget.models import BankAccount

register = template.Library()

@register.inclusion_tag('budget/accounts.html', takes_context=True)
def tag_accounts_list(context):
	user = context['user']
	return {
		'accounts_list': BankAccount.objects.filter(is_active=True, profile=user.profile).order_by("-created_at"),
	}