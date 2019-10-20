# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from builtins import Exception, ValueError
from datetime import datetime

import bs4, requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.views import View

from shpacoo_portal.forms import UserCreateForm, LoginForm, AddArtistForm
from shpacoo_portal.models import Artist, Album, ScrappedData


class TestView(View):
    def get(self, request):
        return render(request, 'test.html')


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('display-albums')
        return redirect('login')


class UserCreateView(View):

    def get(self, request):
        form = UserCreateForm()
        return render(request, 'user_create.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('login')
        return redirect('register')


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
        return redirect('display-albums')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('display-albums')
        return redirect('login')


class LogoutView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('index')
        return redirect('login')


class AddArtistView(View):

    # def get(self, request):
    #     form = AddArtistForm()
    #     return render(request, 'add_artist.html', {'form': form})

    def post(self, request):
        form = AddArtistForm(request.POST)
        if form.is_valid():
            artist_name = form.cleaned_data['name']
            try:
                artist = Artist.objects.get(name=artist_name)
                artist.user.add(request.user)
            except ObjectDoesNotExist:
                Artist.objects.create(name=artist_name)
                artist = Artist.objects.get(name=artist_name)
                artist.user.add(User.objects.get(username=request.user))
                self.find_picture(artist_name)
            return redirect('find-albums')

    def find_picture(self, artist_name):
        pass


# class FindAlbumView(View):
#
#     def get(self, request, id):
#         HipHopDxScraper.get(self, request, id)
#         GeniusScraper.get(self, request, id)
#         return redirect('display-albums')


class FindAlbumsView(View):

    def get(self, request):
        HipHopDxAllScraper.get(self, request)
        GeniusAllScraper.get(self, request)
        artists = Artist.objects.filter(user__username=request.user)
        for artist in artists:
            try:
                scrapped_data = ScrappedData.objects.filter(artist_name=artist.name)
                for single_scrapped_data in scrapped_data:
                    Album.objects.get_or_create(
                        title=single_scrapped_data.title,
                        release_date=single_scrapped_data.release_date,
                        artist=artist
                    )
            except ObjectDoesNotExist:
                pass
        return redirect('display-albums')


class HipHopDxAllScraper(View):

    def get(self, request):
        current_month = datetime.now().strftime('%m')[1:]
        for month in range(int(current_month), 13):
            scrapped_website = requests.get(f'https://hiphopdx.com/release-dates?month={month}')
            soup = bs4.BeautifulSoup(scrapped_website.text, features='html.parser')
            albums = soup.select('.album a')
            for album in albums:
                if album.em:
                    print('start')
                    # sought_artist = Artist.objects.get(id=id)
                    artist_name = ' '.join(album.em.text.split())
                    release_date = album.find_all_previous('p')[1].text
                    if re.search(r'[A-Z]{1}[a-z]{2}\W[0-9]{1,2}', release_date):
                        release_date = datetime.strptime(release_date + ' 2019', '%b %d %Y').strftime('%Y-%m-%d')
                        print('1 ---', release_date)
                    else:
                        all_previous_p_tags = album.find_all_previous('p')
                        for p_tag in all_previous_p_tags:
                            release_date = re.search(r'[A-Z]{1}[a-z]{2}\W[0-9]{1,2}', str(p_tag))
                            if release_date:
                                print('pre 2', release_date[0])
                                if release_date[0].split()[0].lower() in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                                          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                                    release_date = datetime.strptime(release_date[0] + ' 2019', '%b %d %Y').strftime(
                                        '%Y-%m-%d')
                                    print('2 ---', release_date)
                                    break
                    print(album.em.text)
                    print(album.text)
                    title = ''
                    album_name = list(album.text)
                    print(album_name)
                    count = len(artist_name) - 1
                    print('count -', count)
                    for j in album.text[::-1]:
                        try:
                            if j == artist_name[count]:
                                print(j, artist_name[-1])
                                album_name.pop()
                                count -= 1
                            else:
                                break
                        except IndexError:
                            pass
                    title = ''.join(album_name)
                    print(title)
                    print('3 ---', release_date)
                    print(artist_name)
                    print('end')
                    try:
                        ScrappedData.objects.get(title=title, release_date=release_date)
                    except (ObjectDoesNotExist, MultipleObjectsReturned):
                        ScrappedData.objects.create(title=title, release_date=release_date, artist_name=artist_name)


class GeniusAllScraper(View):

    def get(self, request):
        current_month = datetime.now().strftime('%m')[1:]
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        # sought_artist = Artist.objects.get(id=id)
        for month in range(int(current_month), 13):
            try:
                scrapped_website = requests.get(
                    f"https://genius.com/Genius-{months[month]}-2019-album-release-calendar-annotated")
            except IndexError:
                break
            soup = bs4.BeautifulSoup(scrapped_website.text, features='html.parser')
            page = soup.select('p')
            splited_months = page[0].text.split('\n\n')
            month_data = []
            month_data_dict = {}
            for splited_month in splited_months:
                month_data.append(splited_month.split('\n'))
                for day in range(len(month_data)):
                    month_data_dict[month_data[day][0]] = []
                    for album in range(1, len(month_data[day])):
                        month_data_dict[month_data[day][0]].append(month_data[day][album])
            # print(month_data_dict)
            for date, albums in month_data_dict.items():
                for album in albums:
                    artist_name = album.split(' - ')[0]
                    # print('name ' + sought_artist.name.lower() + ' ' + artist_name.lower())
                    # artist_name = artist_name.lower()
                    if date != 'TBA' and date:
                        try:
                            release_date = datetime.strptime(date.split('/')[0] + ' ' + date.split('/')[1] + ' 2019', '%m %d %Y').strftime('%Y-%m-%d')
                        except ValueError:
                            print('To fix later - if there is one more <br> between albums it takes the name as a date')
                    else:
                        release_date = '2222-11-11'
                    title = ' '.join(album.split(' - ')[1:(-1 if '/' in album.split(' - ')[-1] else 0)])
                    print(title)
                    print(release_date)
                    print(artist_name)
                    try:
                        ScrappedData.objects.get(title=title, release_date=release_date)
                    except (ObjectDoesNotExist, MultipleObjectsReturned):
                        ScrappedData.objects.create(title=title, release_date=release_date, artist_name=artist_name)


# class HipHopDxScraper(View):
#
#     def get(self, request, id):
#         current_month = datetime.now().strftime('%m')[1:]
#         for month in range(int(current_month), 13):
#             scrapped_website = requests.get(f'https://hiphopdx.com/release-dates?month={month}')
#             soup = bs4.BeautifulSoup(scrapped_website.text, features='html.parser')
#             albums = soup.select('.album a')
#             for album in albums:
#                 if album.em:
#                     sought_artist = Artist.objects.get(id=id)
#                     if ''.join(album.em.text.lower().split()) == ''.join(sought_artist.name.lower().split()):
#                         release_date = album.find_all_previous('p')[1].text
#                         if re.search(r'[A-Z]{1}[a-z]{2}\W[0-9]{1,2}', release_date):
#                             release_date = datetime.strptime(release_date + ' 2019', '%b %d %Y').strftime('%Y-%m-%d')
#                         else:
#                             all_previous_p_tags = album.find_all_previous('p')
#                             for p_tag in all_previous_p_tags:
#                                 release_date = re.search(r'[A-Z]{1}[a-z]{2}\W[0-9]{1,2}', str(p_tag))
#                                 if release_date:
#                                     release_date = datetime.strptime(release_date[0] + ' 2019', '%b %d %Y').strftime('%Y-%m-%d')
#                                     break
#                         title = album.text.replace(album.em.text, '')
#                         print(title)
#                         print(release_date)
#                         print(sought_artist.name)
#                         Album.objects.get_or_create(title=title, release_date=release_date, artist=sought_artist)
#                         # print(albums)
#                         # except Exception as e:
#                         #     print(e)
#                         # except ObjectDoesNotExist:
#                         #     Album.objects.create(title=title, release_date=date, artist=sought_artist)


# class GeniusScraper(View):
#
#     def get(self, request, id):
#         current_month = datetime.now().strftime('%m')[1:]
#         months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#                   'November', 'December']
#         sought_artist = Artist.objects.get(id=id)
#         for month in range(int(current_month), 13):
#             try:
#                 scrapped_website = requests.get(
#                     f"https://genius.com/Genius-{months[month]}-2019-album-release-calendar-annotated")
#             except IndexError:
#                 break
#             soup = bs4.BeautifulSoup(scrapped_website.text, features='html.parser')
#             page = soup.select('p')
#             splited_months = page[0].text.split('\n\n')
#             month_data = []
#             month_data_dict = {}
#             for splited_month in splited_months:
#                 month_data.append(splited_month.split('\n'))
#                 for day in range(len(month_data)):
#                     month_data_dict[month_data[day][0]] = []
#                     for album in range(1, len(month_data[day])):
#                         month_data_dict[month_data[day][0]].append(month_data[day][album])
#             # print(month_data_dict)
#             for date, albums in month_data_dict.items():
#                 for album in albums:
#                     artist_name = album.split(' - ')[0].lower()
#                     print('name ' + sought_artist.name.lower() + ' ' + artist_name.lower())
#                     if sought_artist.name.lower() == artist_name.lower():
#                         if date != 'TBA' and date:
#                             release_date = datetime.strptime(date.split('/')[0] + ' ' + date.split('/')[1] + ' 2019', '%m %d %Y').strftime('%Y-%m-%d')
#                         else:
#                             '2222-11-11'
#                         title = ' '.join(album.split(' - ')[1:(-1 if '/' in album.split(' - ')[-1] else 0)])
#                         print(title)
#                         print(release_date)
#                         print(sought_artist.name)
#                         Album.objects.get_or_create(title=title, release_date=release_date, artist=sought_artist)
                        #     print(album)
                        # except Exception as e:
                        #     print(e)
                        # except ObjectDoesNotExist:
                        #     Album.objects.create(title=title, release_date=release_date, artist=sought_artist)
            

class DisplayAlbumsView(View):

    def get(self, request):
        artists = Artist.objects.filter(user__username=request.user)
        albums = Album.objects.filter(artist__in=artists)
        form = AddArtistForm()
        return render(request, 'display_album.html', {'artists': artists, 'albums': albums, 'user': request.user, 'add_artist_form': form})


class DeleteArtistView(View):

    def get(self, request, id):
        Artist.objects.get(id=id).delete()
        return redirect('display-albums')



