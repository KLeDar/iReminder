import datetime
from itertools import count

from django.contrib.auth import login
from django.http import HttpResponseNotFound, HttpResponse, Http404, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from reminders import functions
from reminders.models import Reminder_Category, Reminder
from django.contrib.auth.models import User
from .forms import RegistrationForm


# Create your views here.

class GuestView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('main')
        context = {'title': 'Веб-приложение "iReminder"',
                   }
        return render(request, 'guest.html', context=context)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm
        context = {'title': 'Регистрация нового пользователя',
                   'form': form
                   }
        return render(request, 'registration.html', context=context)

    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            form.clean()
            login(request, form.save())
            return HttpResponseRedirect('/')
        else:
            context = {'title': 'Регистрация нового пользователя',
                       'form': form,
                       }
            return render(request, 'registration.html', context=context)


class MainView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_superuser:
            return redirect('/admin/')
        print(Reminder.objects.filter(category__author=get_user_id(request)))
        print("@@@")
        print(len(Reminder.objects.filter(category__author=get_user_id(request))))
        print(datetime.datetime.now())
        context = {'title': 'Главное меню',
                   'user_fullname': get_header_name(request),
                   'all_reminders': len(get_user_reminder(request)),
                   'near_of_date_reminders': len(get_user_reminder(request)
                                                 .filter(date_of_completion=datetime.datetime.now())),
                   'out_of_date_reminders': len(get_user_reminder(request)
                                                .exclude(date_of_completion=datetime.datetime.now())
                                                .exclude(date_of_completion=None)),
                   'completed_reminders': len(get_user_reminder(request)
                                              .filter(completed=1)),
                   'categories': get_categories(request),
                   }
        return render(request, 'main.html', context=context)

    def post(self, request):
        if request.method == "POST":
            functions.create_reminder_category(name=request.POST.get('name'),
                                               author=get_user_id(request))
            return HttpResponseRedirect(reverse('main'))


class RemindersView(View):
    def get(self, request, category_id):
        if not Reminder_Category.objects.filter(id=category_id):
            raise Http404
        if not get_categories(request):
            raise Http404

        context = {'title': 'События',
                   'category_id': category_id,
                   'user_fullname': get_header_name(request),
                   'current_category_name': Reminder_Category.objects.get(id=category_id),
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

    def delete(request, category_id, reminder_id):
        functions.delete_reminder(reminder_id)
        return HttpResponseRedirect(reverse('reminders', kwargs={'category_id': category_id}))


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404, Страница не найдена! Возможно вы зашли в не свои события!')


def custom_handler500(request):
    return HttpResponse("Ошибка 500,либо что-то сломалось, либо вы зашли в не свои события!")


def get_user_id(request):
    return User.objects.get(username=request.user.get_username())


def get_categories(request):
    return Reminder_Category.objects.filter(author_id=get_user_id(request))


def get_user_reminder(request):
    return Reminder.objects.filter(category__author=get_user_id(request))


def get_header_name(request):
    if request.user.get_full_name():
        return request.user.get_full_name()
    else:
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
