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

    def test_a_download(self):
        with self.assertRaises(NoneError):
            roller.Roller(self.filebad).download()
        with self.assertRaises(HTTPError):
            roller.Roller(self.filebad, url='https://web.uvic.ca/~austinb/')
        with self.assertRaises(ValueError):
            roller.Roller(self.filebad, url='not/a/server')

        self.roller1.download(self.server)
        assert(os.path.exists(self.file1))

    def test_b_parser(self):
        """ Test file to be run locally with numpy. Commented out to avoid adding numpy as a dependency. """
        # The parser computes variances and means WAY better than I expected. We're talking
        # numpy mean: 5.029483161648177 ; parser mean: 5.029483161648176
        # numpy variance: 8.261168000112667 ; parser variance: 8.261168000112676
        pass
        """ test_parse """
        # stat = self.roller1.parse()
        # self.assertEqual(round(stat['CPU_current Variance'], 6), 8.261166)
        # self.assertEqual(round(stat['CPU_current Mean'], 6), 5.029483)

    def test_timeframe(self):
        self.assertEqual(self.roller1.time_pattern, '\d\d:\d\d.\d\d')
        self.assertEqual(len(self.roller1.time_range("04:20.04", "04:20.10")), 6)

    def test_z_delete(self):
        self.roller1.download(self.server)
        self.roller1.delete()
        assert(not os.path.exists(self.file1))

if __name__ == '__main__':
    unittest.main()
