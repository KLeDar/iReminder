from reminders.models import *

'''
def authorization(login, password):
    try:
        return User.objects.get(login=login, password=password)
    except User.DoesNotExist:
        return None
'''

def create_reminder(name, category_id, completed):
    Reminder.objects.create(name=name,
                            category_id=category_id,
                            completed=completed)
