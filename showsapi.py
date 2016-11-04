import eztvit
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

class ShowAPI(object):
    '''
    Api for getting magent links of new episodes.
    '''

    api = eztvit.EztvIt()

    def __init__(self, shows, callback):
        '''
        Initializes the class.

        :param dict shows: Dictionary of shows to scan.
        :param func callback: Callback function to run on each episode found.
        '''
        self._callback = callback
        self._shows = shows

    def check_torrents(self, torrents):
        '''
        Returns the largest torrent of each list of torrents.
        (Larger file size == Higher quality)

        :param list torrents: list of torrents
        '''
        largest = None
        for torrent in torrents:
            if largest is None or torrent['size_mb'] > largest['size_mb']:
                largest = torrent
        return largest

    def check_season(self, show, season, episodes, new_season=False):
        '''
        Checks a season for new episodes, and runs the callback on each
        new episode found.

        :param str show: show name
        :param int season: currently checked season
        :param dict episodes: a dictionary of all episodes in the current season
        :param bool new_season: wether or not this is a new season(compared to
        what is written in the shows.json)
        '''
        for episode, torrents in episodes.items():
            if new_season or episode >= self._shows[show]['episode']:
                torrent = self.check_torrents(torrents)
                self._callback(show, season, episode, torrent)

    def check_show(self, show, seasons):
        '''
        Checks show for new episodes/seasons.

        :param str show: show name
        :param dict seasons: all show's seasons.
        '''
        for season, episodes in seasons.items():
            if season == self._shows[show]['season']:
                self.check_season(show, season, episodes)
            elif season > self._shows[show]['season']:
                self.check_season(show, season, episodes, new_season=True)

    def run(self):
        '''
        Runs the checker.
        '''
        for show in self._shows:
            seasons = self.api.get_episodes(show)
            self.check_show(show, seasons)
