from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.core.mail import send_mail
from django.urls import reverse

from .models import User

from .forms import RegisterForm, AuthorizeForm

from mysite.settings import EMAIL_HOST_USER

import uuid



# Класс для обработки url регистрации
class Register(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            'form': form,
            'standard_form': True
        }

        return render(request, 'authtest/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        context = {
            'form': form,
            'standard_form': True,
        }

        if form.is_valid():
            user = form.save()
            code = str(uuid.uuid4())
            while User.objects.filter(code=code):
                code = str(uuid.uuid4())

            user.code = code
            user.save()

            url = request.build_absolute_uri(reverse('verify', kwargs={'code': code}))
            send_mail('Подтверждение аккаунта', 
                      f'Подтвердите аккаунт путём перехода по данной ссылке: {url}', 
                      EMAIL_HOST_USER, 
                      [form.cleaned_data['email']], 
                      fail_silently=False
            )

            messages.add_message(request, messages.SUCCESS, 'Письмо для подтверждения аккаунта отправлено на вашу почту.')
            return redirect('authorize')
        else:
            messages.add_message(request, messages.ERROR, 'Проверьте данные формы.')
        
        return render(request, 'authtest/register.html', context)


# Класс для обработки url авторизации
class Authorize(View):
    def get(self, request, *args, **kwargs):
        form = AuthorizeForm()
        context = {
            'form': form,
            'standard_form': False,
        }

        return render(request, 'authtest/authorize.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        form = AuthorizeForm(request.POST)
        context = {
            'form': form,
            'standard_form': False
        }

        username = request.POST['username']
        password = request.POST['password']
        
        user = User.objects.filter(username=username)
        if user and user[0].is_verify:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Ошибка авторизации.')
        else:
            print(f'Аккаунт не подтверждён: {user[0].is_verify}')
            messages.add_message(request, messages.ERROR, 'Сначала - подтвердите вашу почту.')

        return render(request, 'authtest/authorize.html', context)



# Класс для обработки url подтверждения пользователя по коду из почты
class Verify(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(code=kwargs['code'])
        if user:
            user[0].is_verify = True
            user[0].code = None

            user[0].save()

            return HttpResponse(f'Аккаунт успешно подтверждён. Можете вернуться к процессу <a href=\"{request.build_absolute_uri(reverse("authorize"))}\">авторизации</a> на сайте.')
        else:
            print('Пользователя нет')
            return HttpResponse('Неверный код.')
