import eztvit
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

class ShowAPI(object):

    api = eztvit.EztvIt()

    def __init__(self, shows, callback):
        self._callback = callback
        self._shows = shows

    def check_torrents(self, torrents):
        largest = None
        for torrent in torrents:
            if largest is None or torrent['size_mb'] > largest['size_mb']:
                largest = torrent
        return largest

    def check_season(self, show, season, episodes, new_season=False):
        for episode, torrents in episodes.items():
            if new_season or episode >= self._shows[show]['episode']:
                torrent = self.check_torrents(torrents)
                self._callback(show, season, episode, torrent)

    def check_show(self, show, seasons):
        for season, episodes in seasons.items():
            if season == self._shows[show]['season']:
                self.check_season(show, season, episodes)
            elif season > self._shows[show]['season']:
                self.check_season(show, season, episodes, new_season=True)

    def run(self):
        for show in self._shows:
            seasons = self.api.get_episodes(show)
            self.check_show(show, seasons)
