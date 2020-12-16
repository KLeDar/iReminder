from datetime import datetime
from itertools import count

from django import template
from reminders.models import *

register = template.Library()


@register.filter
def count_reminders(category_id):
    return len(Reminder.objects.filter(category_id=category_id).exclude(completed=1))


@register.filter
def is_out_of_today(date_of_completion):
    #print('date_of_completion -> ', date_of_completion.day)
    #print('datetime.datetime.today() ->', datetime.now())
    #print(date_of_completion == datetime.now())
    if date_of_completion == datetime.now():
        return 'out_of_today'


# доделать красвый фильтр
@register.filter
def is_completed(reminder_id):
    for rem in Reminder.objects.filter(id=reminder_id):
        if rem.completed == 1:
            dict_completed = {'checked': 'checked', 'value': '0'}
            return True
        else:
            dict_completed = {'value': '1'}
            return False
        set(dict_completed)
        print(dict_completed)
        print(dict_completed)

