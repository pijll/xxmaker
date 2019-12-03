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
        os.path.isfile('1849.pdf')

if __name__ == '__main__':
    unittest.main()
