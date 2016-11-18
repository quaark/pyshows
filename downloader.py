import re
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable the Insecure Connection warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class UTorrent(object):
    '''
    Class for connecting to utorrent.
    '''

    UTORRENT_URL = 'http://%s:%d/gui/'
    REGEX_UTORRENT_TOKEN = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'

    def __init__(self, url='127.0.0.1', port=57274, user='', password=''):
        '''
        Initializes the class and creates a new session with the
        utorrent server.

        :param str url: url of the server
        :param int port: port of the server
        :param str user: user of the server
        :param str password: password of the server
        '''
        self._url = self.UTORRENT_URL % (url, port)
        self._auth = requests.auth.HTTPBasicAuth(user, password)
        self._start_session()

    def _start_session(self):
        '''
        Starts a session with utorrent server,
        Authenticates the session and saves the cookies.
        '''
        token_url = self._url + 'token.html'
        resonse = requests.get(token_url, auth=self._auth)
        self._token = re.search(self.REGEX_UTORRENT_TOKEN, resonse.text).group(1)
        guid = resonse.cookies['GUID']
        self._cookies = dict(GUID=guid)

    def add_torrent(self, link):
        '''
        Adds a torrent for utorrent to download.

        :param str link: Magnet link or file path to add to utorrent
        '''
        params = {'action':'add-url', 'token': self._token}
        files = {'s': link}
        resonse = requests.post(url=self._url,
                                auth=self._auth,
                                cookies=self._cookies,
                                params=params,
                                files=files)
        build = json.loads(resonse.content)['build']
        return build
