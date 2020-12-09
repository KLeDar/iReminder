from itertools import count

from django import template
from reminders.models import *

register = template.Library()


@register.filter
def count_reminders(category_id):
    return len(Reminder.objects.filter(category_id=category_id))
