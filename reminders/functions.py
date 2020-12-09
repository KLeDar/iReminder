from reminders.models import *

'''
def authorization(login, password):
    try:
        return User.objects.get(login=login, password=password)
    except User.DoesNotExist:
        return None
'''


# События


def create_reminder(name, category_id, completed):
    Reminder.objects.create(name=name,
                            category_id=category_id,
                            completed=completed)


def update_reminder(reminder_id, name, category_id, completed):
    Reminder.objects.filter(id=reminder_id).update(name=name,
                                                   category_id=category_id,
                                                   completed=completed)


def delete_reminder(reminder_id):
    Reminder.objects.filter(id=reminder_id).delete()


# Категории событий

def create_reminder_category(name, author):
    Reminder_Category.objects.create(name=name,
                                     author=author)
