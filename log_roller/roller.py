import os
import urllib.request
from urllib.error import HTTPError

LOG_DIRECTORY = 'logs/'


class Roller(object):
    def __init__(self, filename, url='https://web.uvic.ca/~austinb/'):
        self._filename = filename
        self._url = url

    @property
    def filename(self):
        return self._filename

    @property
    def url(self):
        return self._url

    def download(self):
        if not os.path.exists(LOG_DIRECTORY):
            os.mkdir(LOG_DIRECTORY)
        try:
            urllib.request.urlretrieve(self.url+self.filename, self.filename)
            os.rename(self.filename, 'logs/%s' % self.filename)
        except (ValueError, HTTPError) as ex:
            raise ex
