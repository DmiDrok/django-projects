from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class Home(View, LoginRequiredMixin):
    login_url = reverse_lazy('register')

    def get(self, request, *args, **kwargs):
        return HttpResponse('Главная страница')
