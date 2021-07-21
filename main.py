from bs4 import BeautifulSoup
import vk_api
from vk_api import audio
from yandex_music import Client
import os
import requests
from time import time

import config


def openDir(str):
    name_dir = str
    path = r'C:\Users\balahnin\PycharmProjects\download\\' + name_dir
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)


def replaceSymbols(str):
    str = str.replace('/', ' ').replace('"', ' ').replace('«', '\'').replace('»', '\'').replace('\\',
                                                                                                " ").replace(
        ":", ' ').replace("?", ' ').replace('<', '\'').replace('>', '\''
                                                                    '').replace('|', " ")
    return str


def downloadYandexMusic():
    openDir('music_yandex')
    start = time()
    client = Client.from_credentials('chvu111@yandex.ru', '207chVu22')
    tracks = client.users_likes_tracks()
    for track in tracks:
        fetch_artists = track.fetch_track()['artists']
        artists = ''
        for artist in fetch_artists:
            if (artists == ''):
                artists = artist['name']
            else:
                artists += ', ' + artist['name']
        name = track.fetch_track()['title']
        version = track.fetch_track()['version']
        if (version != None):
            fullname = artists + ' - ' + name + ' (' + version + ').mp3'
        else:
            fullname = artists + ' - ' + name + '.mp3'
        fullname = replaceSymbols(fullname)
        print(fullname)
        track.fetch_track().download(fullname)
    end = time()
    print(end - start)


def downloadVKMusic():
    openDir('music_vk')
    REQUEST_STATUS_CODE = 200
    login = '+79805471561'  # Номер телефона
    password = config.password  # Пароль
    my_id = '176813461'  # Ваш id vk
    vk_session = vk_api.VkApi(login=login, password=password)
    vk_session.auth()
    vk = vk_session.get_api()
    # классам
    vk_audio = audio.VkAudio(vk_session)
    start = time()
    for i in vk_audio.get(owner_id=my_id):
        try:
            r = requests.get(i["url"])
            if r.status_code == REQUEST_STATUS_CODE:
                with open(i["artist"] + '-' + i["title"] + '.mp3', 'wb') as output_file:
                    output_file.write(r.content)
        except OSError:
            print(i["artist"] + '-' + i["title"])
    end = time()
    print(end - start)


downloadVKMusic()
