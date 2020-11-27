from reminders.models import *


def create_reminder(name, category_id):
    Reminder.objects.create(name=name,
                            category_id=category_id)
