from itertools import count

from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from reminders.models import User, Reminder_Category, Reminder


class GuestView(View):
    def get(self, request):
        context = {'title': 'Guest',
                   }
        return render(request, 'guest.html', context=context)


class AuthView(View):
    def get(self, request):
        context = {'title': 'Authorization',
                   }
        return render(request, 'auth.html', context=context)


class RegistrationView(View):
    def get(self, request):
        context = {'title': 'Registration',
                   }
        return render(request, 'registration.html', context=context)


class MainView(View):
    def get(self, request):
        context = {'title': 'Main',
                   'categories': Reminder_Category.objects.all(),
                   # 'count': count(Reminder_Category.objects.get()),
                   }
        return render(request, 'main.html', context=context)


class RemindersView(View):
    def get(self, request):
        context = {'title': 'Reminders',
                   }
        return render(request, 'reminders.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Ошибка 404, Простите извините!')


def custom_handler500(request):
    return HttpResponse("Ой, что то сломалось... Ошибка 500, Простите извините!")
