from django import template
from datetime import timedelta, datetime
from django.utils import timezone

register = template.Library()
@register.filter
def formatted_date(value):
    if not value:
        return 'N/A'
    today = datetime.now().date()
    value = timezone.localtime(value)

    print(value.date(), today)
    if value.date() == today:
        return value.strftime('Today at %I:%M %p')
    elif value.date() == today - timedelta(days=1):
        return value.strftime('Yesterday at %I:%M %p')
    elif value.date() >= today - timedelta(days=7):
        return value.strftime('%A at %I:%M %p')
    else:
        return value.strftime('%B %d, %Y at %I:%M %p')