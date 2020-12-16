from reminders.models import *


# События

def create_reminder(name, category_id, completed):
    Reminder.objects.create(name=name,
                            category_id=category_id,
                            completed=completed)


def update_reminder(reminder_id, name, date_of_completion):
    Reminder.objects.filter(id=reminder_id).update(name=name,
                                                   date_of_completion=date_of_completion)


def delete_reminder(reminder_id):
    Reminder.objects.filter(id=reminder_id).delete()


def complete_reminder(reminder_id, value):
    Reminder.objects.filter(id=reminder_id).update(completed=value)


# Категории событий

def create_reminder_category(name, author):
    Reminder_Category.objects.create(name=name,
                                     author=author)


def update_reminder_category(category_id, name):
    Reminder_Category.objects.filter(id=category_id).update(name=name)
                                                 # author=author)


def delete_reminder_category(category_id):
    Reminder_Category.objects.filter(id=category_id).delete()
