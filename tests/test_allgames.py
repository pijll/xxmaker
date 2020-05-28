import unittest
import sys
import os

import game.g18africa
import game.g18al
import game.g1800
import game.g1836jr
import game.g1849


class AllGames(unittest.TestCase):
    def test_18Africa(self):
        # arrange
        try:
            os.remove('18Africa.ps')
            os.remove('18Africa.pdf')
        except OSError:
            pass

        # act
        game.g18africa.create_18africa()

        # assert
        self.assertTrue(os.path.isfile('18Africa.pdf'))

    def test_18AL(self):
        # arrange
        try:
            os.remove('18AL.ps')
            os.remove('18AL.pdf')
        except OSError:
            pass

        # act
        game.g18al.create_18al()

        # assert
        self.assertTrue(os.path.isfile('18AL.pdf'))

    def test_1800(self):
        # arrange
        try:
            os.remove('1800.ps')
            os.remove('1800.pdf')
        except OSError:
            pass

        # act
        game.g1800.create_1800()

        # assert
        self.assertTrue(os.path.isfile('1800.pdf'))

    def test_1836Jr(self):
        # arrange
        try:
            os.remove('1836jr.ps')
            os.remove('1836jr.pdf')
        except OSError:
            pass

        # act
        game.g1836jr.create_1836jr()

        # assert
        self.assertTrue(os.path.isfile('1836jr.pdf'))

    def test_1849(self):
        # arrange
        sys.path.insert(1, '../bin/pnp/1849')
        import game.g1849

        try:
            os.remove('1849.ps')
            os.remove('1849.pdf')
        except OSError:
            pass

        # act
        game.g1849.create_1849()

        # assert
        self.assertTrue(os.path.isfile('1849.pdf'))


if __name__ == '__main__':
    unittest.main()
