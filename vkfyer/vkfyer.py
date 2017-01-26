# -*- coding: utf-8 -*-

import sys
import spotipy
import spotipy.util as util
import spotipy.client
import vk_api
from models import VkAudio, SpotifyAudio

try:
    input = raw_input
except NameError:
    pass


class VkFyer:
    SPOTIFY_SCOPE = "user-library-modify user-library-read playlist-modify-public playlist-modify-private " + \
                    "playlist-read-collaborative playlist-read-private"

    SPOTIFY_PLAYLIST_NAME = "Imported from VK.com"
    SPOTIFY_PLAYLIST_LINK = "https://open.spotify.com/user/{login}/playlist/{id}"

    _spotify_login = None
    _spotify_client = None

    _vk_token = None
    _vk_client = None

    def __init__(self, spotify_login, vk_token):
        self._spotify_login = spotify_login
        self._vk_token = vk_token

    def authorize_clients(self):
        return self._authorize_spotify() and self._authorize_vkontakte()

    def _authorize_spotify(self):
        token = util.prompt_for_user_token(self._spotify_login, self.SPOTIFY_SCOPE)

        if token is not None:
            self._spotify_client = spotipy.Spotify(auth=token)
            return True
        else:
            return False

    def _authorize_vkontakte(self):
        self._vk_client = vk_api.VkApi(token=self._vk_token)

        try:
            api = self._vk_client.get_api()
            api.users.get()
        except vk_api.ApiError as error_msg:
            print(error_msg)
            return False

        return True

    def get_vk_audio(self, owner_id=None, offset=0):
        result = []
        api = self._vk_client.get_api()

        # TODO: improve search when > 5k
        try:
            audio = api.audio.get(owner_id=owner_id, count=5000, offset=offset)
        except vk_api.ApiError as e:
            print(e.error.get("error_msg"))
            exit()

        for track in audio["items"]:
            result.append(VkAudio(track))

        return result

    def find_spotify_track(self, audio):
        search_query = "artist:%s %s" % (audio.artist, audio.title)

        try:
            search_items = self._spotify_client.search(q=search_query, type="track").get("tracks").get("items")
        except spotipy.client.SpotifyException:
            return None

        if len(search_items) > 0:
            return SpotifyAudio(search_items[0])

        return None

    def create_playlist(self):
        playlist = self._spotify_client.user_playlist_create(self._spotify_login, self.SPOTIFY_PLAYLIST_NAME)
        playlist_link = self.SPOTIFY_PLAYLIST_LINK.format(login=self._spotify_login, id=playlist.get('id'))

        return playlist, playlist_link

    def add_tracks_to_playlist(self, playlist_id, tracks):
        imported = self._spotify_client.user_playlist_add_tracks(self._spotify_login, playlist_id, tracks)

        if 'snapshot_id' in imported:
            return True

        return False

    @staticmethod
    def draw_progress(status, total, count):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('%s .. [%s] %s%s\r' % (status, bar, percents, '%'))
        sys.stdout.flush()
