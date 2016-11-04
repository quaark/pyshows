import requests
import re
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Torrent(object):
    def __init__(self, build):
        self._build = build

    def __repr__(self):
        return '<Torrent: %d>' % self._build

    def __str__(self):
        return repr(self)


class UTorrent(object):

    UTORRENT_URL = 'http://%s:%s/gui/'
    REGEX_UTORRENT_TOKEN = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'

    def __init__(self, url='127.0.0.1', port='57274', user='', password=''):
        self._url = self.UTORRENT_URL % (url, port)
        self._auth = requests.auth.HTTPBasicAuth(user, password)
        self._start_session()

    def _start_session(self):
        token_url = self._url + 'token.html'
        r = requests.get(token_url, auth=self._auth)
        self._token = re.search(self.REGEX_UTORRENT_TOKEN, r.text).group(1)
        guid = r.cookies['GUID']
        self._cookies = dict(GUID=guid)

    def add_torrent(self, link):
        params = {'action':'add-url','token': self._token}
        files = {'s': link}
        r = requests.post(url=self._url,
                          auth=self._auth,
                          cookies=self._cookies,
                          params=params,
                          files=files)
        build = json.loads(r.content)['build']
        return Torrent(build)
