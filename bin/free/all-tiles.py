import Game
import Company
import Output
import Train
import Paper
import Colour
import Private
import Tile
import Map
import Hexag
from City import City, Town
import Stockmarket



game = Game.Game(name="tile_roster")
for tile in Tile.Tile.all.values():
    game.add_tile(tile)

output = Output.Output(game)
output.generate()
