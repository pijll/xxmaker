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
from Hexag import Connect, Hill, Water, Hexag as Hex, Label
from City import City, Town, DoubleCity, TripleCity
import Stockmarket
from Definitions import *


Colour.set_palette(Colour.palette_18al_galt)

game = Game.Game(name="18AL", author='Mark Derrick', credits_file='credits.txt')

abc = Company.Company(name="Atlanta, Birmingham & Coast", abbreviation="ABC",
                      colour=Colour.yellow, logo='free/Atlanta_Birmingham_Coast.png',
                      n_stations=2)
atn = Company.Company(name="Alabama, Tennessee & Northern", abbreviation="ATN",
                      colour=Colour.grey, logo='free/Alabama_Tennessee_Northern.svg', logo_zoom=0.9,
                      n_stations=3)
ln = Company.Company(name="Louisville & Nashville", abbreviation="LN",
                     colour=Colour.pink, logo='free/Louisville_Nashville.svg', logo_zoom=0.75,
                     n_stations=4)
mo = Company.Company(name="Mobile & Ohio", abbreviation="MO",
                     colour=Colour.turquoise, logo='free/Mobile_and_Ohio.png', logo_zoom=0.75,
                     n_stations=4)
tag = Company.Company(name="Tennessee, Alabama & Georgia", abbreviation="TAG",
                      colour=Colour.purple, logo='free/Tennessee_Alabama_Georgia.svg', logo_zoom=0.9,
                      n_stations=2)
wra = Company.Company(name="Western Railway of Alabama", abbreviation="WRA",
                      colour=Colour.orange, logo='free/Western_Railway_Alabama.png',
                      n_stations=4)

game.add_company(abc)
game.add_company(atn)
game.add_company(ln)
game.add_company(mo)
game.add_company(tag)
game.add_company(wra)

# stockmarket = [
#     [60, 67, 71, 76, 82, 90, 100, 112, 126, 142, 160, 180, 200, 225, 250, 275, 300, 325, 350],
#     [53, 60, 66, 70, 76, 82, 90, 100, 112, 126, 142, 160, 180, 200, 220, 240, 260, 280, 300],
#     [46, 55, 60, 65, 70, 76, 82, 90, 100, 111, 125, 140, 155, 170, 185, 200],
#     [39, 48, 54, 60, 67, 71, 76, 82, 90, 100, 110, 120, 130],
#     [32, 41, 48, 55, 62, 67, 71, 76, 82, 90, 100],
#     [25, 34, 42, 50, 58, 65, 67, 71, 75, 80],
#     [18, 27, 36, 45, 54, 63, 67, 69, 70],
#     [10, 20, 30, 40, 50, 60, 67, 68],
#     [None, 10, 20, 30, 40, 50, 60],
#     [None, None, 10, 23, 30, 40, 50],
#     [None, None, None, 10, 20, 30, 40]
# ]
#
# stockmarket = Stockmarket.Stockmarket(stockmarket)
# game.add_stockmarket(stockmarket)
#
# for cell in stockmarket.cells.values():
#     if cell.value <= 30:
#         cell.colour = Colour.brown
#     elif cell.value <= 45:
#         cell.colour = Colour.orange
#     elif cell.value <= 60:
#         cell.colour = Colour.yellow
#     elif cell.column == 6 and cell.row <= 5:
#         cell.is_par = True
#

game.add_train(5, Train.Train("2", Colour.phase_1, "100", rusted_by='4'))
game.add_train(4, Train.Train("3", Colour.phase_2, "180", rusted_by='6'))
game.add_train(3, Train.Train("4", Colour.phase_2, "300", rusted_by='7'))
game.add_train(2, Train.Train("5", Colour.phase_3, "450"))
game.add_train(1, Train.Train("6", Colour.phase_3, "630"))
game.add_train(1, Train.Train("7", Colour.phase_3, "700"))
game.add_train(5, Train.Train("4D", Colour.phase_4, "800"))

game.add_private(Private.Private('Tuscumbia Railway', 20, 5,
                                 image=''))
game.add_private(Private.Private('South & North Alabama RR', 40, 10,
                                 'Place coal field token.',
                                 image='misc/carriages/hopper.svg'))
game.add_private(Private.Private('Brown & Sons Lumber Co', 70, 15,
                                 'Place Lumber Terminal tile.',
                                 image='misc/Wood.svg'))
game.add_private(Private.Private('Memphis & Charleston RR', 100, 20,
                                 'Bonus routes for trains.',
                                 image='misc/Star_badge.svg'))
game.add_private(Private.Private("New Decatur Yards", 120, 20,
                                 "Purchase train for 50%.",
                                 image='misc/Train.png'))

SE, S, SW, NW, N, NE = Hexag.tile_sides(Hexag.VERTICAL)

Tile.Tile(441, Colour.phase_1, City('A', value=10), Connect('A', S), Label('B'))
Tile.Tile(445, Colour.phase_1, Connect(SW, SE, Town(value=20, name='Lumber', name_location=(0, -.9))))
Tile.Tile(142, Colour.phase_2, Town('A'), Connect(N, S), Connect('A', NW))
Tile.Tile(143, Colour.phase_2, Town('A'), Connect(N, 'A'), Connect(NW, 'A'), Connect(NE, 'A'))
Tile.Tile(144, Colour.phase_2, Town('A'), Connect(S, 'A'), Connect(NW, 'A'), Connect(NE, 'A'))
Tile.Tile(442, Colour.phase_2, Connect(NW, SE, City('A', value=30)), Connect('A', S), Connect('A', NE), Label('B'))
Tile.Tile(443, Colour.phase_2, Connect(NW, SE, City('A', value=30)), Connect(NE, SW), Connect('A', S), Label('M'))
Tile.Tile(444, Colour.phase_3, Connect(NW, SE, City('A', value=50)), Connect(NE, SW), Connect('A', S), Label('BM'))
Tile.Tile(446, Colour.phase_4, Connect(S, N, TripleCity(value=70)), Connect(NW, SE), Connect(SW, NE), Label('B'))

tiles_numbers = [3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 57, 57, 57, 57, 58, 58, 58, 441, 445,
                 14, 14, 14, 14, 15, 15, 15, 15, 16, 17, 19, 20, 23, 23, 23, 23, 24, 24, 24, 24, 25,
                 26, 27, 28, 29, 142, 142, 143, 143, 144, 144, 442, 443,
                 39, 40, 41, 41, 41, 42, 42, 42, 43, 43, 44, 45, 45, 46, 46, 47, 47,
                 63, 63, 63, 63, 63, 63, 63, 70, 444, 444,
                 446]

for t in tiles_numbers:
    if t in Tile.Tile.all:
        game.add_tile(Tile.Tile.all[t])
    else:
        print(f"OOPS tile {t}")


out = Output.Output(game=game)
out.generate()