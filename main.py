# -*- coding: utf-8 -*-

from vkfyer import VkFyer
import os
import re

try:
    input = raw_input
except NameError:
    pass


def set_env(filename=".spotify_app"):
    setting_re = re.compile("^([A-Z_]+)=(.*?)$")

    with open(filename) as file:
        for setting_line in file.readlines():
            key, value = re.findall(setting_re, setting_line)[0]
            os.environ[key] = value



def welcome():
    welcome_message = "Привет, этот скрипт поможет тебе испортировать свои аудиозаписи из ВК в плейлист Spotify"

    help_message = "После ввода логина от Спотифай - отркоется браузер, " \
                   "нужно будет дать доступ приложению и вставить конечную ссылку ниже..\n"

    print("%s\n%s" % (welcome_message, help_message))


def ask_credentials():
    return input("Введи свой логин Spotify: "), input("Введи свой токен ВК [https://vk.cc/2kMG8k]: ")

if __name__ == "__main__":
    set_env()

    welcome()
    spotify_login, vk_token = ask_credentials()

    vkfyer = VkFyer(spotify_login=spotify_login, vk_token=vk_token)

    if vkfyer.authorize_clients():
        print(u"\nВы успешно авторзировались.")
    else:
        print(u"Не получилось авторизироваться..")
        exit()

    audios = vkfyer.get_vk_audio()
    print("Получено %d аудизоаписей из ВКонтакте" % len(audios))

    found = []
    for progress, audio in enumerate(audios):
        VkFyer.draw_progress("Поиск песен в Spotify", len(audios), progress + 1)

        search = vkfyer.find_spotify_track(audio)
        if search is not None:
            found.append(search)

    print("\nПоиск завершен, найдено: %d, не найдено: %d" % (len(found), len(audios) - len(found)))

    playlist, playlist_url = vkfyer.create_playlist()
    print("\nПлейлист создан: %s" % playlist_url)

    chunks = range(0, len(found), 100)

    for i, m in enumerate(chunks):
        chunk = map(lambda track: track.id, found[m:m + 100])
        VkFyer.draw_progress("Добавление песен в плейлист", len(found), i * 100 + len(chunk))

        vkfyer.add_tracks_to_playlist(playlist.get('id'), chunk)

    print("\nГотово!")