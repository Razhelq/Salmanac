# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from datetime import datetime

import bs4, requests
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


from shpacoo_portal.forms import UserCreateForm, LoginForm, AddArtistForm
from shpacoo_portal.models import Artist


class TestView(View):
    def get(self, request):
        return render(request, 'test.html')


class UserCreateView(View):

    def get(self, request):
        form = UserCreateForm()
        return render(request, 'user_create.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('login')
        return redirect('user-create')


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
        return redirect('add-artist')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('add-artist')
        return redirect('login')


class AddArtistView(View):

    def get(self, request):
        form = AddArtistForm()
        return render(request, 'add_artist.html', {'form': form})

    def post(self, request):
        form = AddArtistForm(request.POST)
        if form.is_valid():
            artist_name = form.cleaned_data['name']
            artist = Artist.objects.create(name=artist_name)
            artist.user.add(User.objects.get(username=request.user))
            self.find_picture(artist_name)
            return redirect('test')

    def find_picture(self, artist_name):
        pass


class FindAlbumView(View):

    def get(self, request, id):
        """
        check what is current month
        for each upcoming month
            scrap website with bs4
            find any matchin record
            if there is matching record:
                get title and release date
                create_record()
        :return:
        """
        current_month = datetime.now().strftime('%m')[1:]
        for month in range(int(current_month), 13):
            scrapped_website = requests.get(f'https://hiphopdx.com/release-dates?month={month}')
            soup = bs4.BeautifulSoup(scrapped_website.text, features='html.parser')
            albums = soup.select('.album a')
            for album in albums:
                if album.em:
                    # print(len(album.find_all_previous('p')))
                    date = album.find_all_previous('p')[1].text
                    if re.search(r'[A-Z]{1}[a-z]{2}\W[0-9]{1,2}', date):
                        print(date)
                    else:
                        all_previous_p_tags = album.find_all_previous('p')
                        for p_tag in all_previous_p_tags:
                            date = re.search(r'[A-Z]{1}[a-z]{2}\W[0-9]{1,2}', str(p_tag))
                            if date:
                                print(date[0])
                                break
                            # print(re.search(r'[a-zA-Z]{3}\W[0-9]{1,2}', str(i)))
                        # print(re.search(r'[a-zA-Z]{3}\W[0-9]{1,2}', aaa))
                    print(album.text.replace(album.em.text, ''))
                    print(album.em.text)






































