from itertools import count

from django.http import HttpResponseNotFound, HttpResponse, Http404, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# Create your views here.
from reminders import functions
from reminders.models import Reminder_Category, Reminder
import requests
from django.contrib.auth.models import User


class GuestView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('main')
        context = {'title': 'Веб-приложение "iReminder"',
                   }
        return render(request, 'guest.html', context=context)


class RegistrationView(View):
    def get(self, request):
        context = {'title': 'Регистрация нового пользователя',
                   }
        return render(request, 'registration.html', context=context)


class MainView(View):
    def get(self, request):
        if not get_username(request):
            raise Http404

        # counts = {object.pk: object.category_id for object in Reminder.objects.all()}
        print(Reminder_Category.objects.filter(author_id=User.objects.get(username=get_username(request))))
        # print(len(counts))
        context = {'title': 'Главное меню',
                   'categories': get_categories(request),
                   # 'count': count(Reminder.objects.id('1')),
                   }
        return render(request, 'main.html', context=context)


class RemindersView(View):
    def get(self, request, category_id):
        if not Reminder_Category.objects.filter(id=category_id):
            raise Http404
        if not get_categories(request):
            raise Http404
        context = {'title': 'События',
                   'categories': get_categories(request),
                   'reminders': Reminder.objects.filter(category_id=category_id),
                   }
        return render(request, 'reminders.html', context=context)

    def post(self, request, category_id):
        if request.method == "POST":
            functions.create_reminder(name=request.POST.get('name'),
                                      category_id=category_id,
                                      completed=0)
            return HttpResponseRedirect(reverse('reminders', kwargs={'category_id': category_id}))


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404, Страница не найдена! Возможно вы зашли в не свои события!')


def custom_handler500(request):
    return HttpResponse("Ошибка 500,либо что-то сломалось, либо вы зашли в не свои события!")


def get_categories(request):
    return Reminder_Category.objects.filter(author_id=User.objects.get(username=get_username(request)))


def get_username(request):
    return request.user.username


'''
class AuthView(View):
    def get(self, request):
        context = {'title': 'Authorization',
                   }
        return render(request, 'auth.html', context=context)



    def post(self, request):
        if request.method == "POST":
            login = request.POST.get('login')
            functions.authorization(login=login,
                                    password=request.POST.get('password'))
            return HttpResponseRedirect(reverse('main', login))
'''
