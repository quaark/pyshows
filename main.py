#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
import json
from downloader import UTorrent
from showsapi import ShowAPI
from config import UTORRENT_CREDENTIALS


class ShowDownloader(object):
    def __init__(self):
        self.get_shows_json()
        self.utorrent = UTorrent(**UTORRENT_CREDENTIALS)
        self.showsapi = ShowAPI(self.shows, self.download_episode)

    def get_shows_json(self):
        shows_json = open('shows.json', 'rb')
        self.shows = json.load(shows_json)
        shows_json.close()

    def download_episode(self, show, season, episode, torrent):
        print 'Downloading %s' % torrent['release']
        self.utorrent.add_torrent(torrent['download']['magnet'])
        if season == self.shows[show]['season']:
            if episode >= self.shows[show]['episode']:
                self.shows[show]['episode'] = episode + 1
        elif season > self.shows[show]['season']:
            self.shows[show]['season'] = season
            self.shows[show]['episode'] = episode + 1

    def run(self):
        self.showsapi.run()
        shows_json = open('shows.json', 'wb')
        json.dump(self.shows, shows_json, indent=4, sort_keys=True)
        shows_json.close()


def main():
    s = ShowDownloader()
    s.run()

if __name__ == '__main__':
    main()
