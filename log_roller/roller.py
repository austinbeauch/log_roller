import os
import urllib.request
from urllib.error import HTTPError

__doc__ = """
Main data parser file. At least to start, files are never fully loaded into memory, as this library is intended
for parsing large log files on systems with hardware limitations.
"""


class Roller(object):
    def __init__(self, file_path, url=None, auto_download=True):
        """
        :param file_path: Log file path. Locally stored if url is None
        :param url: URL of data file. If None, assume the file is stored locally until otherwise specified
        :param auto_download: Automatically download the file when url is specified and the file currently doesn't exist
        """
        self._file_path = file_path
        self._filename = os.path.basename(file_path)
        self._url = url

        if url is not None and not os.path.exists(self._file_path) and auto_download:
            self.download(url)

    @property
    def filepath(self):
        return self._file_path

    @property
    def filename(self):
        return self._filename

    @property
    def url(self):
        return self._url

    def delete(self):
        """Delete the file associated with the Roller object"""
        os.remove(self.filepath)

    def download(self, url):
        """
        Downloads filename from url and moves into the specified data directory.
        File left in working directory if data directory is NONE.
        :param url: (str) Online location of the file to be downloaded
        """
        self._url = url
        try:
            urllib.request.urlretrieve(self.url + self.filename, self.filename)
            os.rename(self.filename, self.filepath)
        except (ValueError, HTTPError) as ex:
            raise ex

    def parse_keyword(self, key):
        """
        Parses data file in search of specific keywords and extracts numeric value associated immediately after.
        :param key: Searched keyword. Casted to a string to allow regex searching.
        :return:
        """
        # TODO: Extract maximum? Contain all in a list?
        # TODO: Add other methods for more specific cases
        # key = str(key)
        raise NotImplementedError

    def average(self):
        """
        Computes average of numeric values in data file
        :return: (float) Average
        """
        # TODO: Determines if one object will only search for one keyword and compute one average, or be more general
        raise NotImplementedError

    def stdev(self):
        """
        Computes standard deviation of numeric values
        :return: (float) Standard deviation
        """
        # TODO: Compute a rolling std for any values, or just based off an array
        # TODO: Implement own stdev calculator in C, instead of using numpy?
        raise NotImplementedError

    def time_range(self, start, stop):
        """
        Get log lines within a certain time interval.
        Return (log? print? append?) log status' between a start-time and end-time
        :param start: (str) Obtain log lines from start time
        :param stop: (str) Stop getting data.
        :return:
        """
        # TODO: Determine how lines are displayed
        # Perhaps add more parameters to specify if the lines should be written to their own log file or stdout
        raise NotImplementedError

    def get_time(self, time):
        """
        Finds the entry at a specific time. Assumed the time format is identical to the times contained in the file.
        :param time: Time to return/print out
        :return:
        """
        # TODO: convert times to something standard? Detect time format in file once it's initialized
        # TODO: Find first occurrence, or add parameter to find all n occurrences
        raise NotImplementedError

    def find_entry(self, string):
        """
        Find an entry with a specific string. Similar to parse_keyword, but more general and allows searching
        for any string. Extracts the full line.
        :param string: (str) searching string
        """
        # TODO: Find first occurrence of the string, or find all n occurrences
        raise NotImplementedError
