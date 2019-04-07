# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from ShpacooAlmanac.shpacoo_portal.forms import UserCreateForm, LoginForm


class TestView(View):
    def get(self, request):
        return render(request, 'test.html')


class UserCreateView(View):

    def get(self, request):
        form = UserCreateForm()
        return render(request, 'user_create.html', {'form': form})

    def post(self, request):
        form = UserCreateView(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('login')
        return redirect('client-create')


class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return request, 'login.html', {'form': form}

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('test)
        return redirect('login')

