from gamepart import *

import Output
import Colour
from gamepart.Hexag import Connect, Hill, Water, Hexag as Hex, Border
from gamepart.City import City, Town
from Definitions import *
import os


def create_1836jr(output_file='1836jr'):
    credits_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CREDITS.txt')
    game = Game.Game(name="1836Jr", author='David Hecht', credits_file=credits_file)

    ss = Company.Company(name="Staatsspoorwegen", abbreviation="SS",
                         colour=Colour.green, n_stations=2)
    hijsm = Company.Company(name="HIJSM", abbreviation="HIJSM",
                               colour=Colour.red,
                               n_stations=2)
    nrs = Company.Company(name="Nederlandsche Rhijnspoorweg-Maatschappij", abbreviation="NRS",
                               colour=Colour.red,
                               n_stations=3)
    belge = Company.Company(name="Chemins de fer de l'État belge", abbreviation="EB",
                               colour=Colour.red, logo='nonfree/Etat_Belge.png',
                               n_stations=4)
    nord = Company.Company(name="Compagnie du Nord - Belge", abbreviation="Nord",
                               colour=Colour.blue, logo='nonfree/Nord.svg',
                               n_stations=3)
    gcl = Company.Company(name="Grande Compagnie du Luxembourg", abbreviation="GCL",
                               colour=Colour.lightblue, logo='nonfree/Luxembourg.png',
                               n_stations=4)
    ns = Company.Company(name="Nederlandse Spoorwegen", abbreviation='NS',
                         colour=Colour.yellow, logo='nonfree/Nederlandse_Spoorwegen_1946-III.png',
                         n_stations=4)

    game.add_company(ss)
    game.add_company(hijsm)
    game.add_company(nrs)
    game.add_company(belge)
    game.add_company(nord)
    game.add_company(gcl)
    game.add_company(ns)

    E, SE, SW, W, NW, NE = Hexag.tile_sides(HORIZONTAL)

    map = Map.Map(orientation=HORIZONTAL)
    game.add_map(map)

    map.add_hexag(coords="A9", hexag=Hex(Connect(SW, SE, City(name='Leeuwarden', value=10, companies=[ss])), colour=Colour.grey))
    map.add_hexag(coords="A11")
    map.add_hexag(coords="A13", hexag=Hexag.External(name='Hamburg', values=[40,70], links={W, SW}))
    map.add_hexag(coords="B8", hexag=Hex(Town(name='Stavoren'), Town(name='Enkhuizen'), cost=Water("F.80")))
    map.add_hexag(coords="B10", hexag=Hex(City(name='Groningen')))
    map.add_hexag(coords="B12")
    map.add_hexag(coords="C7", hexag=Hex(Border(E, Colour.blue)))
    map.add_hexag(coords="C9")
    map.add_hexag(coords="C11")
    map.add_hexag(coords="D6", hexag=Hex(Connect(SE, SW, City('Amsterdam', value=40, companies=[hijsm])),
                                         colour=Colour.yellow, cost=Water('F.40')))
    map.add_hexag(coords="D8", hexag=Hex(cost=Water("F.40")))
    map.add_hexag(coords="D10", hexag=Hex(cost=Water("F.40")))
    map.add_hexag(coords="D12")
    map.add_hexag(coords="E3", hexag=Hexag.External(name='Harwich', values=['+20', '+30'], colour=Colour.blue, links={E, SE}))
    map.add_hexag(coords="E5", hexag=Hex(City('Rotterdam'), City('Den Haag'), colour=Colour.yellow))
    map.add_hexag(coords="E7", hexag=Hex(City('Utrecht')))
    map.add_hexag(coords="E9")
    map.add_hexag(coords="E11", hexag=Hex(City('Arnhem', companies=[nrs]), City(name='Nijmegen'), colour=Colour.yellow,
                                          cost=Water('F.40')))
    map.add_hexag(coords="E13", hexag=Hexag.External(name='Dortmund', values=[30, 50], links={W}))
    map.add_hexag(coords="F4", hexag=Hex(Town('Vlissingen'), cost=Water('F.40')))
    map.add_hexag(coords="F6", hexag=Hex(cost=Water('F.80')))
    map.add_hexag(coords="F8", hexag=Hex(cost=Water('F.40')))
    map.add_hexag(coords="F10", hexag=Hex(Town('Eindhoven')))
    map.add_hexag(coords="G1", hexag=Hexag.External(name='Dover', values=['+20', '+30'], colour=Colour.blue, links={E, SE}))
    map.add_hexag(coords="G3")
    map.add_hexag(coords="G5")
    map.add_hexag(coords="G7", hexag=Hex(City('Antwerp')))
    map.add_hexag(coords="G9", hexag=Hex(cost=Water('F.40')))
    map.add_hexag(coords="G11", hexag=Hex(cost=Water('F.40')))
    map.add_hexag(coords="H2", hexag=Hex(Town('Brugge')))
    map.add_hexag(coords="H4", hexag=Hex(City('Gent')))
    map.add_hexag(coords="H6", hexag=Hex(Connect(W, NE, City('Bruxelles', companies=[belge])), colour=Colour.phase_1))
    map.add_hexag(coords="H8")
    map.add_hexag(coords="H10", hexag=Hex(City('Maastricht'), City('Li\u00e8ge'), cost=Water('F.40')))
    map.add_hexag(coords="H12", hexag=Hexag.External(name='Cologne', values=[30,50], links={W}))
    map.add_hexag(coords="I3", hexag=Hex(Connect(SW, E, City('Lille', companies=[nord]))))
    map.add_hexag(coords="I5")
    map.add_hexag(coords="I7")
    map.add_hexag(coords="I9", hexag=Hex(City('Namur', companies=[gcl]), cost=Water('F.40')))
    map.add_hexag(coords="I11", hexag=Hex(cost=Hill('F.60')))
    map.add_hexag(coords="J2", hexag=Hexag.External(name='Paris', values=['+20', '+30'], links={NE, E}))
    map.add_hexag(coords="J4")
    map.add_hexag(coords="J6", hexag=Hex(City('Charleroi')))
    map.add_hexag(coords="J8", hexag=Hex(City('Hainaut Coalfields'), cost=Hill('F.60')))
    map.add_hexag(coords="J10", hexag=Hex(cost=Hill('F.60')))
    map.add_hexag(coords="J12", hexag=Hex(cost=Hill('F.60')))
    map.add_hexag(coords="K5")
    map.add_hexag(coords="K7", hexag=Hex(cost=Hill('F.60')))
    map.add_hexag(coords="K9", hexag=Hex(cost=Hill('F.60')))
    map.add_hexag(coords="K11", hexag=Hex(Town('Luxembourg'), Town('Arlon'), cost=Hill('F.60')))
    map.add_hexag(coords="K13", hexag=Hexag.External(name='Strasbourg', values=[40, 70], links={W, NW}))

    stockmarket = [
        [60, 67, 71, 76, 82, 90, 100, 112, 126, 142, 160, 180, 200, 225, 250, 275, 300, 325, 350],
        [53, 60, 66, 70, 76, 82, 90, 100, 112, 126, 142, 160, 180, 200, 220, 240, 260, 280, 300],
        [46, 55, 60, 65, 70, 76, 82, 90, 100, 111, 125, 140, 155, 170, 185, 200],
        [39, 48, 54, 60, 67, 71, 76, 82, 90, 100, 110, 120, 130],
        [32, 41, 48, 55, 62, 67, 71, 76, 82, 90, 100],
        [25, 34, 42, 50, 58, 65, 67, 71, 75, 80],
        [18, 27, 36, 45, 54, 63, 67, 69, 70],
        [10, 20, 30, 40, 50, 60, 67, 68],
        [None, 10, 20, 30, 40, 50, 60],
        [None, None, 10, 23, 30, 40, 50],
        [None, None, None, 10, 20, 30, 40]
    ]

    stockmarket = Stockmarket.Stockmarket(stockmarket)
    game.add_stockmarket(stockmarket)

    for cell in stockmarket.cells.values():
        if cell.value <= 30:
            cell.colour = Colour.brown
        elif cell.value <= 45:
            cell.colour = Colour.orange
        elif cell.value <= 60:
            cell.colour = Colour.yellow
        elif cell.column == 6 and cell.row <= 5:
            cell.is_par = True

    game.add_train(5, Train.Train("2", Colour.phase_1, 80, rusted_by='4'))
    game.add_train(4, Train.Train("3", Colour.phase_2, 180, rusted_by='6'))
    game.add_train(3, Train.Train("4", Colour.phase_2, 300, rusted_by='D'))
    game.add_train(2, Train.Train("5", Colour.phase_3, 450))
    game.add_train(2, Train.Train("6", Colour.phase_3, 630))
    game.add_train(5, Train.Train("D", Colour.phase_3, 1100, exchange_price=800))

    game.add_private(Private.Private("Beurtvaart Amsterdam-Haarlem", 20, 5))
    game.add_private(Private.Private("Enkhuizen-Stavoren Ferry", 40, 10, 'Place free tile on B8'))
    game.add_private(Private.Private("Charbonnages du Hainaut", 70, 15, 'Place tile and token on J8 for F.60'))
    game.add_private(Private.Private("Grand-Central Belge", 110, 20, 'Echange for 10% Etat Belge'))
    game.add_private(Private.Private("Chemins de Fer Luxemburgeois", 160, 25, 'Comes with 10% GCL'))
    game.add_private(Private.Private("Chemin de Fer de Lille \\\\a Valenciennes", 220, 30,
                                     "President's share of the Nord."))

    tiles_numbers_1830 = [1, 2, 3, 3, 4, 4, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 55, 56, 57, 57,
                     57, 57, 58, 58, 69,
                     14, 14, 14, 15, 15, 16, 18, 19, 20, 23, 23, 23, 24, 24, 24, 25, 26, 27, 28, 29,
                     53, 54, 59,
                     39, 40, 41, 41, 42, 42, 43, 43, 44, 45, 45, 46, 46, 47, 61, 61, 62, 63, 63, 63,
                     64, 65, 66, 67, 68, 70]

    Tile.Tile.all[54].hexag.label.text = 'AMS'
    Tile.Tile.all[62].hexag.label.text = 'AMS'

    for t in tiles_numbers_1830:
        if t in Tile.Tile.all:
            game.add_tile(Tile.Tile.all[t])
        else:
            print(f"OOPS tile {t}")

    out = Output.Output(game=game, output_file=output_file)
    out.generate()


if __name__ == '__main__':
    create_1836jr()
