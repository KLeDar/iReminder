"""iReminder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views

from reminders.views import GuestView, RegistrationView, MainView, RemindersView, RemindersFilterView, \
    RemindersSearchView, delete_reminder, complete_reminder, delete_category, update_category, update_reminder,\
    custom_handler403, custom_handler404, custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GuestView.as_view(), name='guest'),
    path('main/', MainView.as_view(), name='main'),
    # Работа с категориями
    path('main/<int:category_id>/', RemindersView.as_view(), name='reminders'),
    path('main/delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('main/update_category/<int:category_id>/', update_category, name='update_category'),
    # Работа с событиями
    path('main/<int:category_id>/update_reminder/<int:reminder_id>', update_reminder, name='update_reminder'),
    path('main/<int:category_id>/delete_reminder/<int:reminder_id>', delete_reminder, name='delete_reminder'),
    path('main/<int:category_id>/complete_reminder/<int:reminder_id>', complete_reminder, name='complete_reminder'),
    # Поиск и фильтрация
    path('main/search/', RemindersSearchView.as_view(), name='search'),
    path('main/filter/<str:filter_name>', RemindersFilterView.as_view(), name='filter'),
    # Процессы аутентификации
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Сброс пароля через email
    #path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    #path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500
