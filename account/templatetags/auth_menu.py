from django import template

register = template.Library()

@register.inclusion_tag('account/auth_menu.html', takes_context=True)
def tag_account_menu(context):
	request = context['request']
	return {
		'is_authenticated': request.user.is_authenticated,
		'username': request.user.email,
	}