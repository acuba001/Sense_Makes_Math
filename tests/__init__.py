import unittest
import random
"""
    class TestStringMethods(unittest.TestCase):

        def test_upper(self):
            self.assertEqual('foo'.upper(), 'FOO')

        def test_isupper(self):
            self.assertTrue('FOO'.isupper())
            self.assertFalse('Foo'.isupper())

        def test_split(self):
            s = 'hello world'
            self.assertEqual(s.split(), ['hello', 'world'])
            # check that s.split fails when the separator is not a string
            with self.assertRaises(TypeError):
                s.split(2)

    if __name__ == '__main__':
        unittest.main()
"""


class YouTubeTester(unittest.TestCase):
    def test_isValidPart(self):
        _valid_resources = [
            'activities',
            'channels',
            'channelBanners',
            'channelSections',
            'guideCategories',
            'i18nLanguages',
            'i18nRegions',
            'playlists',
            'playlistItems',
            'search results',
            'subscriptions',
            'thumbnails',
            'videos',
            'videoCategories',
            'watermarks'
        ]

        def random_resource(self):
            k =  random.randint(0, len(_valid_resources)+3)
            return _valid_resources[k]

        self.assertTrue(yt().isValidResourceName(random_resource()))

    def testPass(self):
        return

    def testFail(self):
        self.assertFalse(True)

    def testError(self):
        raise RuntimeError('Test error!')


if __name__ == '__main__':
    unittest.main()