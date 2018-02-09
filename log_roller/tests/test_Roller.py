import unittest
import os
from log_roller import roller
from urllib.error import HTTPError
from ..error import NoneError


class RollerTest(unittest.TestCase):
    def setUp(self):
        self.file1 = 'log_1.log'
        self.filebad = 'log_55.log'
        self.server = 'https://web.uvic.ca/~austinb/'
        self.roller1 = roller.Roller(self.file1)

    def test_init(self):
        self.assertEqual(self.roller1.filename, 'log_1.log')
        self.assertEqual(self.roller1.url, None)

        roller.Roller(self.file1, self.server)
        assert (os.path.exists(self.file1))

        roll = roller.Roller('path/to/file.log', auto_download=False)
        self.assertEqual(roll.filename, 'file.log')
        self.roller1.delete()

    def test_download(self):
        with self.assertRaises(NoneError):
            roller.Roller(self.filebad).download()
        with self.assertRaises(HTTPError):
            roller.Roller(self.filebad, 'https://web.uvic.ca/~austinb/')
        with self.assertRaises(ValueError):
            roller.Roller(self.filebad, 'not/a/server')

        self.roller1.download(self.server)
        assert(os.path.exists(self.file1))
        self.roller1.delete()

    def test_delete(self):
        self.roller1.download(self.server)
        self.roller1.delete()
        assert(not os.path.exists(self.file1))

if __name__ == '__main__':
    unittest.main()
