from reminders.models import *


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


def complete_reminder(reminder_id):
    Reminder.objects.filter(id=reminder_id).update(complete=1)


# Категории событий

def create_reminder_category(name, author):
    Reminder_Category.objects.create(name=name,
                                     author=author)


def update_reminder_category(category_id, name):
    Reminder.objects.filter(id=category_id).update(name=name)
                                                 # author=author)


def delete_reminder_category(category_id):
    Reminder.objects.filter(id=category_id).delete()
