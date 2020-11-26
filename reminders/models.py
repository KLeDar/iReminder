from django.db import models


class User(models.Model):
    login = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=20)


class Reminder_Category(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Reminder(models.Model):
    name = models.CharField(max_length=50)
    completed = models.IntegerField()
    date_of_completion = models.DateField()
    category = models.ForeignKey(Reminder_Category, on_delete=models.CASCADE)

'''

User.objects.create(login='kled',
                    password='1234',
                    name='Лавришко Данил Евгеньевич',
                    email="danil.lavrishko2014@yandex.ru")
Reminder_Category.objects.create(name='Курсовая', author=User.objects.get(login='kled'))
Reminder.objects.create(name='Сдача курсача',
                        completed=0,
                        date_of_completion="2020-12-10",
                        category=Reminder_Category.objects.get(name='Курсовая'))
                        
                        '''
