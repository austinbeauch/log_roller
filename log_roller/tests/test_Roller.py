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

        self.assertEqual(roller.Roller("~/path/to/log.log").filepath, os.getenv('HOME')+"/path/to/log.log")

    def test_adownload(self):
        with self.assertRaises(NoneError):
            roller.Roller(self.filebad).download()
        with self.assertRaises(HTTPError):
            roller.Roller(self.filebad, 'https://web.uvic.ca/~austinb/')
        with self.assertRaises(ValueError):
            roller.Roller(self.filebad, 'not/a/server')

        self.roller1.download(self.server)
        assert(os.path.exists(self.file1))

    def test_zdelete(self):
        # zdelete to run last (unit tests run alphabetically)
        self.roller1.download(self.server)
        self.roller1.delete()
        assert(not os.path.exists(self.file1))

    def test_parser(self):
        self.roller1.download('https://web.uvic.ca/~austinb/')
        stat = self.roller1.parse()
        self.assertEqual(round(stat['CPU_current Variance'], 10), 7.9861807559)
        self.assertEqual(round(stat['CPU_current Mean'], 9), 4.902564777)

    def test_timeframe(self):
        self.assertEqual(len(self.roller1.time_range("4:20.04", "4:20.10")), 6)


if __name__ == '__main__':
    unittest.main()
