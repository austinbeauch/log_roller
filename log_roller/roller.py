import os
import re
import urllib.request
from urllib.error import HTTPError
from ..error import NoneError

__doc__ = """
Main data parser file. At least to start, files are never fully loaded into memory, as this library is intended
for parsing large log files on systems with hardware limitations.
"""


class Roller(object):
    def __init__(self, file_path, time_format="hh:mm.ss", pipe="|", url=None, auto_download=True):
        """
        :param file_path: Relative file path.
        :param url: Web address of data file. If None, assume the file is stored locally until otherwise specified.
        :param auto_download: Automatically download the file when url is specified and the file doesn't exist locally.
        """
        # TODO: Add a time format parameter
        if file_path.split('/')[0] == '~':
            self.file_path = file_path.replace('~', os.getenv("HOME"))
        else:
            self.file_path = file_path

        self.filename = os.path.basename(file_path)
        self.url = url
        self._time_format = time_format
        self.time_pattern = _time_form(time_format)
        self.pipe = pipe

        if url is not None and not os.path.exists(self.file_path) and auto_download:
            self.download(url)

    def parse(self):
        """
        General purpose parser method. Generates dictionaries of keywords; keeping running values of times, lines
        averages, variances, standard deviations and more in the future.

        The main purpose of parse, and all of log_roller, is to run through large data files without loading them
        into memory. This also means numeric values contained in the file are not fully stored either. Everything
        is kept as running calculations to reduce memory usage.

        Early stages will split lines by the object's pipe string, and assume that time is always the first entry, along
        with other assumptions based off the files generated in log_generator.py but future versions will be more
        flexible with whatever none-standard format is thrown at the parser.

        Variance and mean accuracy tested accurate to 10 decimal places against NumPy's variance method. NumPy values
        are generated locally to avoid adding NumPy as a requirement.

        :return data: dictionary containing all information
        """
        # TODO: Refine this to be a general parser
        data = {'Lines': 0}
        x_squared = {}
        log_data = open(self.file_path, 'r')
        for line in log_data:
            data["Lines"] += 1
            # time, level, info = line.split('|')

            # TODO: Add more customizability to regex searching
            m = re.search('(.*): (\d+\.?\d*)', line.split(self.pipe)[-1])
            if m is None:
                continue  # No match

            value = float(m.group(2))
            total = m.group(1) + " Total"
            counts = m.group(1) + " Counts"
            mean = m.group(1) + " Mean"
            variance = m.group(1) + " Variance"

            if total not in data:
                x_squared[m.group(1)] = 0
                data[total] = 0
                data[counts] = 0
                data[mean] = 0
                data[variance] = 0

            data[total] += value
            data[counts] += 1
            data[mean] = (data[total] / data[counts])
            x_squared[m.group(1)] += value**2
            data[variance] = (x_squared[m.group(1)] / data[counts]) - data[mean]**2

        log_data.close()
        return data

    def delete(self):
        """Delete the file associated with the Roller object"""
        os.remove(self.file_path)

    def download(self, url=None):
        """
        Downloads Roller filename from url.
        :param url: (str) Online location of the file to be downloaded
        """
        if url is None and self.url is None:
            raise NoneError(self.filename)
        elif url is not None:
            self.url = url
        try:
            urllib.request.urlretrieve(self.url + self.filename, self.filename)
            os.rename(self.filename, self.file_path)
        except (ValueError, HTTPError) as ex:
            raise ex

    def parse_keyword(self, key):
        """
        Parses data file in search of specific keywords and extracts numeric value associated immediately after.
        :param key: Searched keyword. Casted to a string to allow regex searching.
        :return data: (dict) Dictionary containing the sum of all the values, the max value, min value, average of the
        set, standard deviation, and the number of occurrences.
        """
        data = {"Total": 0, "Maximum": 0, "Minimum": 0, "Average": 0, "Standard Deviation": 0, "Counts": 0}
        x_squared = 0
        log_data = open(self.file_path, 'r')

        for line in log_data:
            m = re.search(key, line)
            if m is None:
                continue  # No match

            # TODO: Extract value separate from the time
            value = 0
            data["Total"] += value
            data["Counts"] += 1
            data["Average"] = data["Total"] / data["Counts"]
            x_squared += value**2
            data["Variance"] = (x_squared / data["Counts"]) - data["Average"]**2

        return data

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
        Get log lines within a certain time interval. Return log status' between a start-time and end-time. Used for
        examining short time periods. In the context of this library, a low-memory system shouldn't be calling this
        with extremely large time frames that would result in a large return list.
        :param start: (str) Obtain log lines from start time
        :param stop: (str) Stop time, exclusive
        :return lines: (list) List containing each line within the time frame
        """

        start_flag = False
        lines = []
        log_data = open(self.file_path, 'r')
        for line in log_data:
            m = re.search(self.time_pattern, line)
            if m is None:
                continue
            if m.group() == start:
                start_flag = True
            elif m.group() == stop:
                break
            if start_flag:
                lines.append(line.split('\n')[0])
        log_data.close()
        return lines

    def from_time(self, time, repeat=False):
        """
        Finds the entry at a specific time. Assumed the time format is identical to the times contained in the file.
        :param time: Time to return/print out
        :param repeat: Find and return repeated occurrences of a time. Requires running through all lines of the file.
        :return: Line string if repeat is false, else a list containing strings of all matching entries.
        """
        # TODO: Test the list appending/return format
        lines = []
        log_data = open(self.file_path, 'r')

        for line in log_data:
            m = re.search(self.time_pattern, line)
            if m is None:
                continue
            if m.group() == time:
                lines.append(line.split('\n')[0])
                if not repeat:
                    return line.split('\n')[0]

        log_data.close()
        return lines

    def find_entry(self, string):
        """
        Find an entry with a specific string. Similar to parse_keyword, but more general and allows searching
        for any string. Extracts the full line.
        :param string: (str) searching string
        """
        # TODO: Find first occurrence of the string, or find all n occurrences
        raise NotImplementedError


def _time_form(time):
    """
    Incrementally builds up a regex pattern for a given time. Converts digits to the general \d digit match,
    and same for letters. Everything else is left as itself. Intended to match and arbitrary date/time formats.
    Does not reduce anything to metacharacters. Might be an area to improve in the future.
    :param time: (str) Time format to be generalized for regex searching
    :return pattern: (str) pattern string
    """
    # TODO: Support metacharacters
    pattern = ""
    for i in time:
        if i.isdigit() or i == 'h' or i == 'm' or i == 's':
            pattern += '\d'
        elif i.isalnum():
            pattern += '[A-Za-z]'
        else:
            pattern += i
    return pattern
