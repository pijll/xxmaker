import unittest
import sys
import os


class AllGames(unittest.TestCase):
    def test_1849(self):
        # arrange
        sys.path.insert(1, '../bin/free-to-pnp/1849')
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
