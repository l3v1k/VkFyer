# VkFyer
Скрипт для переноса треков из ВК в Спотифай плейлист

# Использование
1. Установить зависимости
 `pip install --upgrade -r requirements.txt`

2. Создать приложение Spotify
**https://developer.spotify.com/my-applications/#!/applications/create**

3. Задать в приложении ***Redirect URIs***
Можно по-моему любую ссылку

4. Создать файл с credentials от Спотифая
    `mv .spotify_app.example .spotify.app` и заменить в файле занчения, главное чтобы  *redirect-uri* полностью сооствествовал, вроде

5. Достать *access_token* от ВК
Авторизироваться ВК через прямую авторизацию **https://vk.cc/2kMG8k** (нужно установить параметры *username* и *password*) или вытащить сниффером из прилы, как хотите

6. Запустить скриптец
`python main.py`
