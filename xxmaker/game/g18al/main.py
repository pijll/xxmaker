import os

from gamepart import *
import Output
import Colour
from gamepart.Hexag import Label
from gamepart.Connect import Connect
from gamepart.City import City, Town, TripleCity
import Palette
from gamepart.IPO import IPO
from gamepart.Token import Token
from gamepart.Trainyard import Trainyard


def create_18al(outfile='18AL'):
    Colour.Colour.palette = Palette.galt_18al
    Colour.alias['par'] = 'grey'
    Colour.alias['private'] = 'lightblue'

    credits_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credits.txt')
    game = Game.Game(name="18AL", author='Mark Derrick', credits_file=credits_file)

    abc = Company.Company(name="Atlanta, Birmingham & Coast", abbreviation="ABC",
                          colour=Colour.yellow, logo='free/Atlanta_Birmingham_Coast.svg',
                          n_stations=2)
    atn = Company.Company(name="Alabama, Tennessee & Northern", abbreviation="ATN",
                          colour=Colour.grey, logo='free/Alabama_Tennessee_Northern.svg', logo_zoom=0.9,
                          n_stations=3)
    ln = Company.Company(name="Louisville & Nashville", abbreviation="LN",
                         colour=Colour.pink, logo='free/Louisville_Nashville.svg', logo_zoom=0.75,
                         n_stations=4)
    mo = Company.Company(name="Mobile & Ohio", abbreviation="MO",
                         colour=Colour.turquoise, logo='free/Mobile_and_Ohio.svg', logo_zoom=0.75,
                         n_stations=4)
    tag = Company.Company(name="Tennessee, Alabama & Georgia", abbreviation="TAG",
                          colour=Colour.purple, logo='free/Tennessee_Alabama_Georgia.svg', logo_zoom=0.9,
                          n_stations=2)
    wra = Company.Company(name="Western Railway of Alabama", abbreviation="WRA",
                          colour=Colour.orange, logo='free/Western_Railway_Alabama.svg',
                          n_stations=4)

    game.add_company(abc)
    game.add_company(atn)
    game.add_company(ln)
    game.add_company(mo)
    game.add_company(tag)
    game.add_company(wra)

    stockmarket = [
        [60, 65, 70, 75, 80, 90, 105, 120, 135, 150, 170, 190, 215, 240, 270, 300],
        [55, 60, 65, 70, 75, 80, 90, 105, 120, 135, 150, 170, 190, 215, 240],
        [50, 55, 60, 65, 70, 75, 80, 90, 105, 120, 135, 150, 170],
        [45, 50, 55, 60, 65, 70, 75, 80, 90, 105, 120],
        [40, 45, 50, 55, 60, 65, 70, 75],
        [35, 40, 45, 50, 55],
        [30, 35, 40, 45, 50],
    ]

    stockmarket = Stockmarket.Stockmarket(stockmarket, has_par_box=True)
    game.add_stockmarket(stockmarket)

    for cell in stockmarket.cells.values():
        if cell.value <= 50:
            cell.colour = Colour.yellow
    stockmarket.cells[5, 4].colour = Colour.yellow
    for cell in [(0, 6), (0, 5), (1, 4), (1, 3), (2, 2)]:
        stockmarket.cells[cell].is_par = True
    stockmarket.cells[0, stockmarket.width-1].text = 'Game over'

    stockmarket.current_round_marker = Misc.RoundIndicator(Colour.phase_1, Colour.phase_2, Colour.phase_3)

    game.add_train(5, Train.Train("2", Colour.phase_1, "100", rusted_by='4',
                                  phase_info='Yellow tiles\n1 OR per SDR\nRRs may buy only one train from bank per turn'))
    game.add_train(4, Train.Train("3", Colour.phase_2, "180", rusted_by='6',
                                  phase_info='Yellow and green tiles\n2 ORs per SDR\nRRs may buy private companies (for 50% to 150%)'))
    game.add_train(3, Train.Train("4", Colour.phase_2, "300", rusted_by='7',
                                  phase_info='2 trains rust\nRRs may buy multiple trains from bank per turn'))
    game.add_train(2, Train.Train("5", Colour.phase_3, "450",
                                  phase_info='Yellow, green, and brown tiles\n3 ORs per SDR\nPrivate companies are removed from play'))
    game.add_train(1, Train.Train("6", Colour.phase_3, "630",
                                  phase_info='3 trains rust\nCoal field tokens are removed from play'))
    game.add_train(1, Train.Train("7", Colour.phase_3, "700",
                                  phase_info='4 trains become obsolete'))
    game.add_train(5, Train.Train("4D", Colour.phase_4, "800",
                                  phase_info='Yellow, green, brown, and grey tiles'))

    game.add_private(Private.Private('Tuscumbia Railway', 20, 5,
                                     image='misc/Crossing.svg'))
    game.add_private(Private.Private('South & North Alabama RR', 40, 10,
                                     'Place coal field token.',
                                     image='misc/carriages/hopper.svg'))
    game.add_private(Private.Private('Brown & Sons Lumber Co', 70, 15,
                                     'Place Lumber Terminal tile.',
                                     image='misc/Wood.svg'))
    game.add_private(Private.Private('Memphis & Charleston RR', 100, 20,
                                     'Bonus:Atlanta-Birmingham +20,\nNashville-Mobile +40.',
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

    game.add_token(Misc.round_indicator_token())
    token = Token(image_file='misc/carriages/hopper.svg', text='+10')
    for _ in 1, 2:
        game.add_token(token)

    game.add_paper(IPO(game), Trainyard(game), Misc.priority_deal())

    out = Output.Output(game=game, output_file=outfile)
    out.generate()
