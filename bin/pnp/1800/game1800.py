import Game
import Company
import Output
import Train
import Misc
import Colour
import Private
import Tile
import Map
import Hexag
from Hexag import Hill, Water, Hexag as Hex, Label
from City import City, Town, DoubleCity
import Stockmarket
from Definitions import *
import os
import Draw
from Draw import FillStyle


def create_1800(output_file='1800'):
    three_players = Draw.Canvas((0,0), 3*mm, 3*mm)
    Draw.triangle(three_players, (1.5*mm, 1.7*mm), 2.8*mm, FillStyle(Colour.grey))

    credits_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CREDITS.txt')
    game = Game.Game(name="1800", author='Antonio Leal', credits_file=credits_file, currency='$')

    cs = Company.Company(name="Colorado and Southern", abbreviation="CS",
                         colour=Colour.green, logo='free/Colorado_and_Southern.png',
                         n_stations=3)
    dr = Company.Company(name="Denver and Rio Grande Western", abbreviation="DR",
                         colour=Colour.red, logo='free/Denver_Rio_Grande.png',
                         n_stations=3)

    # The Colorado & Western does not seem to be a historical company.
    # I've replaced it with the Colorado Midland, based in Colorado Springs
    cm = Company.Company(name="Colorado Midland", abbreviation="CM",
                         colour=Colour.blue, logo='free/Colorado_Midland.png',
                         n_stations=3, marker=three_players)

    game.add_company(cs)
    game.add_company(dr)
    game.add_company(cm)

    SE, S, SW, NW, N, NE = Hexag.tile_sides(Hexag.VERTICAL)

    map2 = Map.Map(orientation=VERTICAL)
    game.add_map(map2)
    map2.add_hexag(coords="A3", hexag=Hexag.External(City(name='Cheyenne', x=0, y=-0.2, name_location=(0, -0.5)),
                                                     links={S}, values=[10, 40, 70], value_location=(0, .4)))
    map2.add_hexag(coords="C3", hexag=Hex(cost=Hill('50')))
    map2.add_hexag(coords="D2", hexag=Hex(Town()))
    map2.add_hexag(coords="D4", hexag=Hex(Town()))
    map2.add_hexag(coords="E1", hexag=Hex(City(companies=[dr])))
    map2.add_hexag(coords="E3", hexag=Hex(City(x=-0.5, y=0.2), City(x=0.5, y=0.2, name='Fort Collins', name_location=(-0.7, -0.6)),
                                          Label('OO', (.6, -.3)), colour=Colour.phase_1))
    map2.add_hexag(coords="E5", hexag=Hex(City(companies=[cs])))
    map2.add_hexag(coords="F2", hexag=Hex(cost=Water('40')))
    map2.add_hexag(coords="F4", hexag=Hex(cost=Water('40')))
    map2.add_hexag(coords="G1", hexag=Hexag.External(links={N}, values=[10, 20, 30]))
    map2.add_hexag(coords="G3", hexag=Hex(City(name='Denver'), cost=Water('40')))
    map2.add_hexag(coords="G5", hexag=Hexag.External(links={N}, values=[10, 20, 30]))
    map2.add_hexag(coords='I3', hexag=Hexag.External(links={N}, values=[20, 30, 40]))

    map2.add_element(Misc.RoundIndicator(Colour.phase_1, Colour.phase_2, Colour.phase_3), 'top right')
    map2.add_element(Misc.Name(game), 'top left')
    game.add_token(Misc.round_indicator_token())

    map3 = Map.Map(orientation=VERTICAL, marker=three_players)
    game.add_map(map3)
    map3.add_hexag(coords="A3", hexag=Hexag.External(City(name='Cheyenne', x=0, y=-0.2, name_location=(0, -0.5)),
                                                     links={S}, values=[10, 40, 70], value_location=(0, .4)))
    map3.add_hexag(coords="C3", hexag=Hex(cost=Hill('50')))
    map3.add_hexag(coords="D2", hexag=Hex(Town()))
    map3.add_hexag(coords="D4", hexag=Hex(Town()))
    map3.add_hexag(coords="E1", hexag=Hex(City(companies=[dr])))
    map3.add_hexag(coords="E3", hexag=Hex(City(x=-0.5, y=0.2), City(x=0.5, y=0.2, name='Fort Collins', name_location=(-0.7, -0.6)),
                                          Label('OO', (.6, -.3)), colour=Colour.phase_1))
    map3.add_hexag(coords="E5", hexag=Hex(City(companies=[cs])))
    map3.add_hexag(coords="F2", hexag=Hex(cost=Water('40')))
    map3.add_hexag(coords="F4", hexag=Hex(cost=Water('40')))
    map3.add_hexag(coords="G1", hexag=Hexag.External(links={N}, values=[10, 20, 30]))
    map3.add_hexag(coords="G3", hexag=Hex(City(name='Denver'), cost=Water('40')))
    map3.add_hexag(coords="G5", hexag=Hexag.External(links={N}, values=[10, 20, 30]))
    map3.add_hexag(coords="H2", hexag=Hexag.External(links={SE}, values=[10, 20, 30]))
    map3.add_hexag(coords="H4", hexag=Hexag.External(links={SW}, values=[10, 20, 30]))
    map3.add_hexag(coords="I3", hexag=Hexag.Hexag(City(name='Colorado Springs', companies=[cm])))

    map2.add_element(Misc.RoundIndicator(Colour.phase_1, Colour.phase_2, Colour.phase_3), 'top right')
    map3.add_element(Misc.Name(game), 'top left')

    stockmarket = [
        [80, 90, 100, 110, 120, 140, 160, 180, 200, 225],
        [70, 80, 90, 100, 110, 120, 140, 160, 180],
        [60, 70, 80, 90, 100, 110, 120],
        [50, 60, 70, 80, 90, 100, 110],
        [40, 50, 60, 70, 80, 90],
        [30, 40, 50, 60, 70],
        [20, 30, 40, 50, 60],
        [10, 20, 30, 40],
    ]

    stockmarket = Stockmarket.Stockmarket(stockmarket)
    game.add_stockmarket(stockmarket)

    for cell in [(3,0), (3,1), (4,1), (5,1), (5,2), (6,2), (7,2)]:
        stockmarket.cells[cell].colour = Colour.yellow

    for cell in [(4,0), (5,0), (6,0), (6,1), (7,0), (7,1)]:
        stockmarket.cells[cell].colour = Colour.orange

    for cell in [(1,3), (2,3), (3,3), (4,3), (5,3)]:
        stockmarket.cells[cell].colour = Colour.lightgreen

    game.add_train(3, Train.Train("2", Colour.phase_1, "$180", rusted_by='4'))
    game.add_train(2, Train.Train("3", Colour.phase_2, "$300", rusted_by='E'))
    game.add_train(1, Train.Train("4", Colour.phase_2, "$430"))
    game.add_train(2, Train.Train("5", Colour.phase_3, "$450"))
    game.add_train(3, Train.Train("2E", Colour.phase_4, "$250"))
    game.add_train(2, Train.Train("3E", Colour.phase_4, "$350"))
    game.add_train(1, Train.Train("2x2E", Colour.phase_4, "$500"))

    game.add_private(Private.Private("Midland Terminal", "$20", "$5"))
    game.add_private(Private.Private("Denver and Salt Lake", "$70", "$10"))
    game.add_private(Private.Private("Rio Grande Southern", "$150", "$20"))
    game.add_private(Private.Private("D & R G W Bond", "$300", "$50"))
    game.add_private(Private.Private("C & S Bond", "$300", "$50"))
    game.add_private(Private.Private("Midland Terminal", "$25", "$5"))
    game.add_private(Private.Private("Denver and Salt Lake", "$70", "$10"))
    game.add_private(Private.Private("C & W Bond", "$300", "$50"))

    game.add_paper(Misc.priority_deal())
    #game.add_paper(Misc.trainyard())

    Tile.Tile(800, Colour.phase_2, Town('A', value=30), Hexag.Connect(SW, NE), Hexag.Connect(S, 'A'),
                            Hexag.Connect(SE, 'A'), label='D&SL', label_location=(-0.3, -0.5))
    Tile.Tile(802, Colour.phase_2, Hexag.Connect(S, N, DoubleCity('A', value=40, name='Denver', name_location=(-0.5, 0.45))),
                            Hexag.Connect(NW, 'A'), Hexag.Connect(NE, 'A'))
    Tile.Tile(803, Colour.phase_3, Hexag.Connect(S, N, DoubleCity('A', value=50, name='Denver', name_location=(-0.5, 0.45))),
                            Hexag.Connect(NW, 'A'), Hexag.Connect(NE, 'A'))
    Tile.Tile(804, Colour.phase_3, City('A', value=40), Hexag.Connect('A', N),
                            Hexag.Connect(NW, 'A'), Hexag.Connect(NE, 'A'))
    Tile.Tile(805, Colour.phase_4, Hexag.Connect(S, N, DoubleCity('A', value=60, name='Denver', name_location=(-0.5, 0.45))),
                            Hexag.Connect(NW, 'A'), Hexag.Connect(NE, 'A'))
    Tile.Tile(806, Colour.phase_4, Town('A', value=10), Hexag.Connect(SW, NE), Hexag.Connect(S, 'A'))
    Tile.Tile(807, Colour.phase_4, Town('A', value=10), Hexag.Connect(SW, NE), Hexag.Connect(SE, 'A'))
    Tile.Tile(808, Colour.phase_4, Town('A', value=10), Hexag.Connect(SW, 'A'), Hexag.Connect(SE, 'A'),
                            Hexag.Connect(S, 'A'))

    tiles_numbers = [3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 12, 12, 16, 18, 19, 23, 24, 25, 26, 27, 28, 29,
                     39, 40, 41, 42, 43, 45, 46, 58, 58, 59, 64, 65, 67, 68, 70, 800, 802, 803, 804, 805, 806, 807, 808]

    for t in tiles_numbers:
        if t in Tile.Tile.all:
            game.add_tile(Tile.Tile.all[t])
        else:
            print(f"OOPS tile {t}")

    # replacement tile for 3-player expansion
    Tile.Tile(802, Colour.phase_2, Hexag.Connect(S, N, DoubleCity('A', value=40, name='Denver', name_location=(-0.5, 0.45), companies=[cm])),
              Hexag.Connect(NW, 'A'), Hexag.Connect(NE, 'A'))

    tiles_numbers_3players = [5, 6, 12, 15, 802, 804]

    for t in tiles_numbers_3players:
        if t in Tile.Tile.all:
            game.add_tile(Tile.Tile.all[t])
        else:
            print(f"OOPS tile {t}")

    out = Output.Output(game=game, output_file=output_file)
    out.generate()


if __name__ == '__main__':
    create_1800('1800')
