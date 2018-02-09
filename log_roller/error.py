"""Roller exception class"""


class NoneError(Exception):
    def __init__(self, file):
        self.file = file

    def __str__(self):
        return 'File: {} has no specified URL and does not exist locally.'.format(self.file)
