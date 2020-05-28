from gamepart import Game
import Output
from gamepart import Tile
import unittest
import os
from gamepart import Misc


class AllTiles(unittest.TestCase):
    def test_alltiles(self):
        game = Game.Game(name="alltiles", author='', credits_file='credits')
        game.add_paper(Misc.priority_deal())
        for tile in Tile.Tile.all.values():
            game.add_tile(tile)

        output = Output.Output(game, output_file='alltiles')
        output.generate()

        self.assertTrue(os.path.isfile('alltiles.pdf'))


if __name__ == '__main__':
    unittest.main()
