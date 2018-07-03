#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
import json
from downloader import Transmission
from showsapi import ShowAPI
from config import TRANSMISSION_SETTINGS, SHOWS_JSON_FILE


class ShowDownloader(object):
    '''
    Main class for downloading new episodes.
    '''

    def __init__(self):
        '''
        Initializes the class.
        Gets show json.
        Initializes Transmission class and ShowAPI class.
        '''
        self.get_shows_json()
        self.transmission = Transmission(**TRANSMISSION_SETTINGS)
        self.showsapi = ShowAPI(self.shows, self.download_episode)

    def get_shows_json(self):
        '''
        Gets show dictionary from the shows json file.
        '''
        shows_json = open(SHOWS_JSON_FILE, 'rb')
        self.shows = json.load(shows_json)
        shows_json.close()

    def download_episode(self, show, season, episode, torrent):
        '''
        Callback for showsapi on each episode.
        Gets the episode and runs the download on transmission.
        Then updates the shows dictionary.

        :param str show: show name
        :param int season: season number
        :param int episode: episode number
        :param dict torrent: torrent dictionary
        '''
        print 'Downloading %s' % torrent['release']
        self.transmission.add_torrent(torrent['download']['magnet'])
        if season == self.shows[show]['season']:
            if episode >= self.shows[show]['episode']:
                self.shows[show]['episode'] = episode + 1
        elif season > self.shows[show]['season']:
            self.shows[show]['season'] = season
            self.shows[show]['episode'] = episode + 1

    def run(self):
        '''
        Runs the api.
        Updates the shows json file when finished.
        '''
        self.showsapi.run()
        shows_json = open(SHOWS_JSON_FILE, 'wb')
        json.dump(self.shows, shows_json, indent=4, sort_keys=True)
        shows_json.close()


def main():
    '''
    Main Function
    '''
    s = ShowDownloader()
    s.run()

if __name__ == '__main__':
    main()
