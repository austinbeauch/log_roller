import unittest
from urllib.error import HTTPError
from log_roller import roller


class RollerTest(unittest.TestCase):

    def setUp(self):
        self.file1 = 'log_1.log'
        self.file2 = 'log_2.log'
        self.filebad = 'log_55.log'
        self.server = 'https://web.uvic.ca/~austinb/'
        self.roller1 = roller.Roller(self.file1)
        self.roller2 = roller.Roller(self.file2, url='not_a_server')

    def test_download(self):
        self.assertEqual(self.roller1.filename, self.file1)
        self.assertEqual(self.roller1.url, self.server)

        with self.assertRaises(ValueError):
            self.roller2.download()
        with self.assertRaises(HTTPError):
            roller.Roller(self.filebad).download()


if __name__ == '__main__':
    unittest.main()
