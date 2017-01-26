class Audio:
    title = None
    artist = None
    duration = None

    def __init__(self):
        pass

    def __str__(self):
        return self.artist + " - " + self.title


class SpotifyAudio(Audio):

    id = None

    def __init__(self, audio):
        self.id = audio.get('id')
        self.artist = audio.get('artists')[0].get('name')
        self.title = audio.get('name')
        self.duration = audio.get('duration_ms')


class VkAudio(Audio):
    def __init__(self, audio):
        self.artist = audio.get('artist')
        self.title = audio.get('title')
        self.duration = audio.get('duration') * 1000
