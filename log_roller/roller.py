"""
Main data parser file. At least to start, files are never fully loaded into memory, as this library is intended
for parsing large log files on systems with hardware limitations.
"""

import os
import urllib.request
from urllib.error import HTTPError

LOG_DIRECTORY = 'logs/'


class Roller(object):
	def __init__(self, filename, url='https://web.uvic.ca/~austinb/', path=LOG_DIRECTORY):
		self._filename = filename
		self._url = url
		self._path = path

	@property
	def filename(self):
		return self._filename

	@property
	def url(self):
		return self._url

	@property
	def path(self):
		return self._path

	def download(self):
		"""
		Downloads filename from url and moves into the specified data directory.
		File left in working directory if data directory is NONE.
		"""

		if not os.path.exists(LOG_DIRECTORY):
			os.mkdir(LOG_DIRECTORY)
		try:
			urllib.request.urlretrieve(self.url + self.filename, self.filename)
			os.rename(self.filename, self.path+self.filename)
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
