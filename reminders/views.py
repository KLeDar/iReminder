import datetime
from django.contrib.auth import login
from django.http import HttpResponseNotFound, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from reminders import functions
from reminders.models import Reminder_Category, Reminder
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.utils import timezone


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
        context = {'title': 'Главное меню',
                   'user_fullname': get_header_name(request),
                   'all_reminders': len(get_user_reminder(request).exclude(completed=1)),
                   'near_of_date_reminders': len(get_user_reminder(request)
                                                 .filter(date_of_completion__gte=timezone.now())
                                                 .exclude(completed=1)),
                   'out_of_date_reminders': len(get_user_reminder(request)
                                                .filter(date_of_completion__lte=timezone.now())
                                                .exclude(date_of_completion=None)
                                                .exclude(completed=1)),
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
                   'header_list': Reminder_Category.objects.get(id=category_id),
                   'categories': get_categories(request),
                   'reminders': Reminder.objects.filter(category_id=category_id).exclude(completed=1),
                   'datetime_now': timezone.now(),
                   'categories_list': True,
                   'add_reminder': True,
                   }
        return render(request, 'reminders.html', context=context)

    def post(self, request, category_id):
        if request.method == "POST":
            functions.create_reminder(name=request.POST.get('name'),
                                      category_id=category_id,
                                      completed=0)
            return HttpResponseRedirect(reverse('reminders', kwargs={'category_id': category_id}))


class RemindersFilterView(View):
    def get(self, request, filter_name):
        """
        if not Reminder_Category.objects.filter(id=category_id):
            raise Http404
        if not get_categories(request):
            raise Http404
        """
        header_list = get_translate_filter(filter_name)
        empty_message = False
        if not get_filter(request, filter_name):
            empty_message = True

        context = {'title': header_list,
                   'user_fullname': get_header_name(request),
                   'header_list': header_list,
                   'categories': get_categories(request),
                   'reminders': get_filter(request, filter_name),
                   'datetime_now': timezone.now(),
                   'categories_list': False,
                   'add_reminder': False,
                   'empty_message': empty_message,
                   }
        return render(request, 'reminders.html', context=context)


class RemindersSearchView(View):
    def get(self, request):
        """
        if not Reminder_Category.objects.filter(id=category_id):
            raise Http404
        if not get_categories(request):
            raise Http404
        'Событий с таким именем не найдено!'
        """
        reminder_name = request.GET.get('search_name')
        header_list = 'События с именем: ' + reminder_name
        empty_message = False
        if not get_user_reminder(request).filter(name__icontains=reminder_name):
            empty_message = True
        context = {'title': header_list,
                   'user_fullname': get_header_name(request),
                   'header_list': header_list,
                   'categories': get_categories(request),
                   'reminders': get_user_reminder(request).filter(name__icontains=reminder_name),
                   'datetime_now': timezone.now(),
                   'categories_list': False,
                   'add_reminder': False,
                   'empty_message': empty_message,
                   }
        return render(request, 'reminders.html', context=context)


############################
#  Операции с категориями  #
############################

def update_category(request, category_id):
    if request.method == "POST":
        functions.update_reminder_category(name=request.POST.get('name'),
                                           category_id=category_id)
        return HttpResponseRedirect(reverse('main'))


def delete_category(request, category_id):
    functions.delete_reminder_category(category_id)
    return HttpResponseRedirect(reverse('main'))


############################
#   Операции с событиями   #
############################

def update_reminder(request, category_id, reminder_id):
    if request.method == "POST":
        date_of_completion = request.POST.get('datetime')
        if not date_of_completion:
            date_of_completion = None
        functions.update_reminder(reminder_id=reminder_id,
                                  name=request.POST.get('name'),
                                  date_of_completion=date_of_completion)
        return HttpResponseRedirect(reverse('reminders', kwargs={'category_id': category_id}))


def delete_reminder(request, category_id, reminder_id):
    functions.delete_reminder(reminder_id)
    if category_id:
        return HttpResponseRedirect(reverse('reminders', kwargs={'category_id': category_id}))
    else:
        return HttpResponseRedirect(reverse('filter', kwargs={'filter_name': 'all'}))


def complete_reminder(request, category_id, reminder_id):
    if request.method == "POST":
        # В value если содержится 0 или False, то выводится None
        value = request.POST.get('checkbox')
        # Исходя из этого, костыль
        if value is None:
            value = False
        functions.complete_reminder(reminder_id=reminder_id, value=value)
        return HttpResponseRedirect(reverse('reminders', kwargs={'category_id': category_id}))


###########################
#     Страницы ошибок     #
###########################

def custom_handler404(request, exception):
    context = {'title': 'Ошибка 404',
               'user_fullname': get_header_name(request),
               'handler_text': 'Ошибка 404, Страница не найдена! Возможно вы не зашли в аккаунт!',
               }
    return HttpResponseNotFound(render(request, 'handler.html', context=context, status=404))


def custom_handler403(request, exception):
    context = {'title': 'Ошибка 403',
               'user_fullname': get_header_name(request),
               'handler_text': 'Ошибка 403, вы пытаетесь войти не туда, ай-ай-ай!',
               }
    return HttpResponse("Ошибка 403, вы пытаетесь войти не туда, ай-ай-ай!")
    #return render(request, 'handler.html', context=context, status=403)


def custom_handler500(request):
    # context = {'title': "Ошибка 404",
    #            'user_fullname': get_header_name(request),
    #            'handler_text': "Ошибка 500, что-то сломалось на сервере!",
    #            }
    return HttpResponse("Ошибка 500, что-то сломалось на сервере!")

###########################
# Вспомогательные функции #
###########################


def get_user_id(request):
    return User.objects.get(username=request.user.get_username())


def get_categories(request):
    return Reminder_Category.objects.filter(author_id=get_user_id(request))


def get_user_reminder(request):
    return Reminder.objects.filter(category__author=get_user_id(request))


def get_filter(request, filter_name):
    if filter_name == 'all':
        return get_user_reminder(request).exclude(completed=1)
    elif filter_name == 'near_of_date':
        return get_user_reminder(request).filter(date_of_completion__gte=timezone.now()).exclude(completed=1)
    elif filter_name == 'out_of_date':
        return get_user_reminder(request).filter(date_of_completion__lte=timezone.now()) \
            .exclude(date_of_completion=None).exclude(completed=1)
    elif filter_name == 'completed':
        return get_user_reminder(request).filter(completed=1)
    else:
        raise Http404


def get_translate_filter(filter_name):
    if filter_name == 'all':
        return 'Все события'
    elif filter_name == 'near_of_date':
        return 'Ближайшие события'
    elif filter_name == 'out_of_date':
        return 'Просроченые события'
    elif filter_name == 'completed':
        return 'Завершённые события'


def get_header_name(request):
    if request.user.get_full_name():
        return request.user.get_full_name()
    else:
        return request.user.username
