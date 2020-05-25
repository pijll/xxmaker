import unittest
import sys
import os


class AllGames(unittest.TestCase):
    def test_18Africa(self):
        # arrange
        sys.path.insert(1, '../bin/pnp/18Africa')
        import game18Africa

        try:
            os.remove('18Africa.ps')
            os.remove('18Africa.pdf')
        except OSError:
            pass

        # act
        game18Africa.create_18africa()

        # assert
        self.assertTrue(os.path.isfile('18Africa.pdf'))

    def test_18AL(self):
        # arrange
        sys.path.insert(1, '../bin/pnp/18AL')
        import game18AL

        try:
            os.remove('18AL.ps')
            os.remove('18AL.pdf')
        except OSError:
            pass

        # act
        game18AL.create_18AL()

        # assert
        self.assertTrue(os.path.isfile('18AL.pdf'))


    def test_1800(self):
        # arrange
        sys.path.insert(1, '../bin/pnp/1800')
        import game1800

        try:
            os.remove('1800.ps')
            os.remove('1800.pdf')
        except OSError:
            pass

        # act
        game1800.create_1800()

        # assert
        self.assertTrue(os.path.isfile('1800.pdf'))

    def test_1836Jr(self):
        # arrange
        sys.path.insert(1, '../bin/pnp/1836Jr')
        import game1836jr

        try:
            os.remove('1836jr.ps')
            os.remove('1836jr.pdf')
        except OSError:
            pass

        # act
        game1836jr.create_game()

        # assert
        self.assertTrue(os.path.isfile('1836jr.pdf'))

    def test_1849(self):
        # arrange
        sys.path.insert(1, '../bin/pnp/1849')
        import game1849

        try:
            os.remove('1849.ps')
            os.remove('1849.pdf')
        except OSError:
            pass

        # act
        game1849.create_1849()

        # assert
        self.assertTrue(os.path.isfile('1849.pdf'))


if __name__ == '__main__':
    unittest.main()
