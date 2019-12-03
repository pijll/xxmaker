import unittest
import sys
import os


class AllGames(unittest.TestCase):
    def test_18Africa(self):
        # arrange
        sys.path.insert(1, '../bin/free-to-pnp/18Africa')
        import game18Africa

        try:
            os.remove('18Africa.ps')
            os.remove('18Africa.pdf')
        except OSError:
            pass

        # act
        game18Africa.create_18Africa()

        # assert
        self.assertTrue(os.path.isfile('18Africa.pdf'))


if __name__ == '__main__':
    unittest.main()
