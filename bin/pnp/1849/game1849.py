import Game
import Company
import Output
import Train
import Colour
import Private
import Tile
import Map
import Hexag
from Hexag import Connect, Hill, Water, Hexag as Hex, WhiteTrack, DottedTrack, Border
from City import City, Town, DoubleCity, TripleCity, QuadCity, Port
import Stockmarket
from Definitions import *
import Misc
import Draw
from Draw import LineStyle, TextStyle
import Font
import os


def draw_token_costs(costs):
    def draw(company, canvas, location):
        x, y = location
        length_of_line = company.n_stations * 2 * logo_radius + (company.n_stations-1) * company.token_interspace
        Draw.line(canvas, (x - length_of_line/2, y + 2*mm),
                  (x + length_of_line/2, y + 2*mm), LineStyle(Colour.black, 1))
        Draw.text(canvas, (x, y+2*mm), costs, TextStyle(Font.normal, Colour.black, 'top', 'center'))
    return draw


def create_1849(output_file='1849'):
    credits_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CREDITS.txt')
    game = Game.Game(name="1849", author='Federico Vellani', credits_file=credits_file)

    afg = Company.Company(name='Azienda Ferroviaria Garibaldi', abbreviation='AFG', colour=Colour.red,
                          n_stations=3, logo='free/Garibaldi.svg', token_costs=draw_token_costs(40))
    ctl = Company.Company(name='Compagnia Trasporti Lilibeo', abbreviation='CTL', colour=Colour.yellow,
                          n_stations=3, logo='free/Lilibeo.svg', token_costs=draw_token_costs(40))
    ift = Company.Company(name='Impresa Ferroviaria Trinacria', abbreviation='IFT', colour=Colour.blue,
                          n_stations=3, logo='free/IFT_Trinacria.svg', token_costs=draw_token_costs(90))
    ata = Company.Company(name='Azienda Trasporti Archimede', abbreviation='ATA', colour=Colour.green,
                          n_stations=3, logo='free/Archimede.svg', token_costs=draw_token_costs(30))
    rcs = Company.Company(name='Rete Centrale Sicula', abbreviation='RCS', colour=Colour.orange,
                          n_stations=3, logo='free/Rete_Centrale_Sicula.svg', token_costs=draw_token_costs(130))
    sfa = Company.Company(name='Societ\u00E0 Ferroviaria Akragas', abbreviation='SFA', colour=Colour.pink,
                          n_stations=3, logo='free/Akragas.svg', token_costs=draw_token_costs(40))

    game.add_company(afg, ctl, ift, ata, rcs, sfa)

    SE, S, SW, NW, N, NE = Hexag.tile_sides(VERTICAL)

    map = Map.Map(orientation=VERTICAL)
    game.add_map(map)

    map.add_hexag(coords='C1', hexag=Hexag.External(Connect(S, SE, City('A'), WhiteTrack),
                                                    name='Trapani', name_location=(-.55, -.35), colour=Colour.phase_4,
                                                    values=[20, 30, 40], value_location=(-.6,0)))
    map.add_hexag(coords='E1', hexag=Hexag.External(City('A', x=0.4, y=0, companies=[ctl]), Connect(N, 'A', WhiteTrack),
                                                    Connect(NE, 'A', WhiteTrack), Connect(SE, 'A', WhiteTrack),
                                                    Connect(S, 'A', WhiteTrack), name='Marsala', name_location=(-.55, -.35),
                                                    colour=Colour.phase_4, values=[20,30,40], value_location=(-.6,0)))
    map.add_hexag(coords='G1', hexag=Hex(Town(name='Mazzara')))

    map.add_hexag(coords='B2', hexag=Hex(Hill(40), Border(SW, Colour.darkblue)))
    map.add_hexag(coords='D2', hexag=Hex(Hill(160)))
    map.add_hexag(coords='F2', hexag=Hex(Hill(160)))
    map.add_hexag(coords='H2')

    map.add_hexag(coords='C3', hexag=Hex(Town(name='Alcamo'), Border(NE, Colour.darkblue)))
    map.add_hexag(coords='E3', hexag=Hex(Hill(80)))
    map.add_hexag(coords='G3', hexag=Hex(Town(name='Castelvetrano')))

    map.add_hexag(coords='B4')
    map.add_hexag(coords='D4', hexag=Hex(Town(name='Partinico'), Hill(40)))
    map.add_hexag(coords='F4', hexag=Hex(Hill(160)))
    map.add_hexag(coords='H4', hexag=Hex(Town(name='Sciacca'), Hill(80)))

    map.add_hexag(coords='A5', hexag=Hexag.External(Port(value=10), links={S}, colour=Colour.lightblue))
    map.add_hexag(coords='C5', hexag=Hex(Connect(NW, SE, City('A', name='Palermo', name_location=(0,.6), value=50, companies=[rcs])),
                                         Connect(N, 'A'), colour=Colour.phase_1, label='P'))
    map.add_hexag(coords='E5', hexag=Hex(Town(name='Corleone'), Hill(160)))
    map.add_hexag(coords='G5', hexag=Hex(Hill(160)))
    map.add_hexag(coords='I5', hexag=Hex(Hill(80)))

    map.add_hexag(coords='D6', hexag=Hex(Border(NE, Colour.darkblue)))
    map.add_hexag(coords='F6', hexag=Hex(Hill(80)))
    map.add_hexag(coords='H6', hexag=Hex(Hill(40)))
    map.add_hexag(coords='J6', hexag=Hex(City(name='Gitgenti', companies=[sfa]), Hill(40)))

    map.add_hexag(coords='C7')
    map.add_hexag(coords='E7', hexag=Hex(Town(name='Termini Imerese')))
    map.add_hexag(coords='G7', hexag=Hex(Hill(80)))
    map.add_hexag(coords='I7', hexag=Hex(Town(name='Canicatti'), Hill(40)))
    map.add_hexag(coords='K7', hexag=Hex(Town(name='Licata')))

    map.add_hexag(coords='D8', hexag=Hex(Border(SW, Colour.red), Border(S, Colour.red), Border(SE, Colour.red)))
    map.add_hexag(coords='F8', hexag=Hex(Hill(160)))
    map.add_hexag(coords='H8', hexag=Hex(City(name='Caltanisetta'), Hill(80)))
    map.add_hexag(coords='J8', hexag=Hex(Hill(160)))
    map.add_hexag(coords='L8')
    map.add_hexag(coords='N8', hexag=Hexag.External(Port(value=20), links={NE}, colour=Colour.lightblue))

    map.add_hexag(coords='C9', hexag=Hex(Town('A', name='St. Stefano', value=10, x=0, y=0.2, value_location=(0.4,0.55)),
                                         Connect(SW, 'A'), Connect(SE, 'A'), Connect(S, 'A', DottedTrack)))
    map.add_hexag(coords='E9', hexag=Hex(Hill(160)))
    map.add_hexag(coords='G9', hexag=Hex(Town(name='Castrogiovanni'), Hill(80)))
    map.add_hexag(coords='I9', hexag=Hex(Town(name='Piazza Armerina'), Hill(160)))
    map.add_hexag(coords='K9', hexag=Hex(Connect(N, S, DottedTrack), Hill(160, x=-0.5, y=0), colour=Colour.phase_1))
    map.add_hexag(coords='M9', hexag=Hexag.External(Connect(NW, SE, DoubleCity('A')), Connect('A', SW, WhiteTrack),
                                                    Connect('A', NE, DottedTrack), Connect('A', N, DottedTrack),
                                                    name='Terranova', colour=Colour.phase_4, values=[20,30,40],
                                                    value_location=(0, 0.75), name_location=(0, 0.42)))

    map.add_hexag(coords='D10', hexag=Hex(Border(SW, Colour.red), Border(S, Colour.red), Border(SE, Colour.red)))
    map.add_hexag(coords='F10', hexag=Hex(Town(name='Troina'), Hill(160)))
    map.add_hexag(coords='H10', hexag=Hex(Hill(40)))
    map.add_hexag(coords='J10', hexag=Hex(Town(name='Caltagirone'), Hill(40)))
    map.add_hexag(coords='L10', hexag=Hex(Hill(160)))
    map.add_hexag(coords='N10', hexag=Hex(Town(name='Vittoria')))

    map.add_hexag(coords='C11')
    map.add_hexag(coords='E11', hexag=Hex(Town(name='Bronte'), Hill(160), Border(N, Colour.red)))
    map.add_hexag(coords='G11', hexag=Hex(Hill(160)))
    map.add_hexag(coords='I11', hexag=Hex(Connect(NW, NE), Colour.phase_1))
    map.add_hexag(coords='K11', hexag=Hex(Hill(40), Border(SW, Colour.red), Border(S, Colour.red)))
    map.add_hexag(coords='M11', hexag=Hex(City('A', name='Ragusa', value=20), Connect('A', NE, DottedTrack),
                                          Connect('A', SW), Hill(40), Border(SE, Colour.red)))
    map.add_hexag(coords='O11')

    map.add_hexag(column=12, row=0, hexag=Hexag.External(Port(value=20), links={SE}, colour=Colour.lightblue))
    map.add_hexag(coords='B12')
    map.add_hexag(coords='D12', hexag=Hex(Hill(160)))
    map.add_hexag(coords='F12', hexag=Hex(Colour.phase_4))

    city = City(name='Catania', companies=[ift], x=0.4, y=0.3)
    map.add_hexag(coords='H12', hexag=Hex(city, Colour.phase_1, Connect(city, SW), label='C'))
    map.add_hexag(coords='J12')
    map.add_hexag(coords='L12', hexag=Hex(Hill(160)))
    map.add_hexag(coords='N12')

    town = Town(name='Milazzo', name_location=(0.5, -0.4), value=10, value_location=(-0.4, 0.3), x=-0.1, y=0.3)
    map.add_hexag(coords='A13', hexag=Hex(town, Connect(town, NW), Connect(town, S), Connect(town, SE), Colour.phase_4))
    map.add_hexag(coords='C13', hexag=Hex(Connect(N, NW), Connect(SW, NE), Colour.phase_4))
    town = Town(name='Taormina', value=10, x=0.2, y=0.1, name_location=(-0.2, -0.7), value_location=(0.4, 0.2))
    map.add_hexag(coords='E13', hexag=Hex(town, Connect(town, NW, DottedTrack), Connect(town, S), Connect(town, NE), Colour.phase_4))
    map.add_hexag(coords='G13', hexag=Hex(Town(name='Acireale', name_location=(0, 0.3), x=0, y=0.5)))
    town = Town(name='Augusta', value=10, x=-0.2, y=0.1, name_location=(.3, -0.4), value_location=(-0.3, 0.2))
    map.add_hexag(coords='K13', hexag=Hex(town, Connect(town, NW), Connect(town, S), Connect(town, SE), Colour.phase_4))
    city = City(name='Siracusa', value=10, companies=[ata])
    map.add_hexag(coords='M13', hexag=Hex(city, Connect(city, NW), Colour.phase_1, label='S'))

    city = City(name='Messina', value=30)
    map.add_hexag(coords='B14', hexag=Hex(city, Connect(city, S), Colour.phase_1, label='M'))
    map.add_hexag(coords='D14')
    # map.add_hexag(coords='L14', hexag=Hexag.External(Port(value=60), links={NW}, colour=Colour.lightblue))
    map.add_hexag(coords='L14', hexag=Hexag.External(links={NW}, colour=Colour.lightblue))

    # This hexag is divided in two, with a line from the NE to the SW corner
    hexag = Hex(Colour.phase_4, Connect(SW, S, WhiteTrack))
    map.add_hexag(coords='A15', hexag=hexag)
    vertices = hexag.vertices()
    ne_corner, sw_corner = vertices[5], vertices[2]
    Draw.line(hexag.draw(), ne_corner.xy(hexag.unit_length), sw_corner.xy(hexag.unit_length), LineStyle(Colour.black, 1))

    map.add_hexag(coords='C15', hexag=Hexag.External(Colour.phase_4, links={N},  name='Calabria', values=[10,30,90]))

    map.add_element(Misc.RoundIndicator(Colour.phase_1, Colour.phase_2, Colour.phase_3), 'bottom right')
    map.add_element(Misc.Name(game=game), 'bottom left')

    game.add_token(Misc.round_indicator_token())
    for hexag in map.hexags.values():
        if hexag.cost:
            token = Draw.Canvas((0,0), 2*logo_radius, 2*logo_radius)
            hexag.cost.draw_at_xy(token, logo_radius, logo_radius)
            game.add_token(token)

    stockmarket = [
        [72,83,95,107,120,133,147,164,182,202,224,248,276,306,340,377],
        [63,72,82,93,104,116,128,142,158,175,195,216,240,266,295,328],
        [57,66,75,84,95,105,117,129,144,159,177,196,218,242,269,298],
        [54,62,71,80,90,100,111,123,137,152,169,187,208,230],
        [52,59,68,77,86,95,106,117,130,145,160,178,198],
        [47,54,62,70,78,87,96,107,118,131,146,162],
        [41,47,54,61,68,75,84,93,103,114,127],
        [34,39,45,50,57,63,70,77,86,95],
        [27,31,36,40,45,50,56],
        ['Closed', 24,27,31]
    ]

    stockmarket = Stockmarket.Stockmarket(stockmarket)
    game.add_stockmarket(stockmarket)

    stockmarket.cells[(1, 11)].is_par = True
    stockmarket.cells[(1, 11)].colour = Colour.phase_3

    stockmarket.cells[(2, 8)].is_par = True
    stockmarket.cells[(2, 8)].colour = Colour.phase_2

    stockmarket.cells[(3, 5)].is_par = True
    stockmarket.cells[(3, 5)].colour = Colour.phase_1

    stockmarket.cells[(4, 2)].is_par = True
    stockmarket.cells[(4, 2)].colour = Colour.phase_1

    stockmarket.cells[(9, 0)].colour = Colour.black

    stockmarket.cells[(0, 13)].colour = Colour.lightblue
    stockmarket.cells[(0, 14)].colour = Colour.lightblue
    stockmarket.cells[(0, 15)].colour = Colour.lightblue
    stockmarket.cells[(1, 13)].colour = Colour.lightblue
    stockmarket.cells[(1, 14)].colour = Colour.lightblue
    stockmarket.cells[(1, 15)].colour = Colour.lightblue
    stockmarket.cells[(2, 13)].colour = Colour.lightblue
    stockmarket.cells[(2, 14)].colour = Colour.lightblue
    stockmarket.cells[(2, 15)].colour = Colour.lightblue

    game.add_train(4, Train.Train('4H', Colour.phase_1, 100, rusted_by='8H', image=''))
    game.add_train(4, Train.Train('6H', Colour.phase_2, 200, rusted_by='10H', image=''))
    game.add_train(3, Train.Train('8H', Colour.phase_2, 350, rusted_by='16H', image=''))
    game.add_train(2, Train.Train('10H', Colour.phase_3, 550, image=''))
    game.add_train(1, Train.Train('12H', Colour.phase_3, 800, image=''))
    game.add_train(5, Train.Train('16H', Colour.phase_3, 1100, image=''))
    game.add_train(2, Train.Train('R6H', Colour.phase_3, 350, image=''))

    game.add_private(Private.Private('Societ\u00E0 Corriere Etnee', 20, 5,
                                     location_on_map='G13', abbreviation='SCE',
                                     image='misc/volcano.svg'))
    game.add_private(Private.Private('Studio di Ingegneria Giuseppe Incorpora', 45, 10,
                                     'Lay or upgrade standard track at half cost.',
                                     image='misc/track.svg'))
    game.add_private(Private.Private('Compagnia Navale Mediterranea', 75, 15,
                                     'Place +20 token on a port.',
                                     image='misc/anchor.svg'))
    game.add_private(Private.Private('Societ\u00E0 Marittima Siciliana', 110, 20,
                                     'Place tile and token on a coastal city.',
                                     image='misc/station.svg'))
    game.add_private(Private.Private("Reale Societ\u00E0 d'Affari", 150, 25,
                                     "Take the president's share\nof the 1st company.",
                                     image='misc/share_certificate.svg'))

    tiles_numbers = [3, 3, 3, 3, 4, 4, 4, 4, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9,
                     58, 58, 58, 58, 73, 73, 73, 73, 74, 74, 74, 77, 77, 77, 77, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,
                     79, 79, 79, 79, 79, 79, 79, 644, 644, 645, 645, 657, 657, 658, 658, 659, 659, 679, 679,
                     23, 23, 23, 24, 24, 24, 25, 25, 26, 27, 28, 29, 30, 31, 624, 650, 651, 653, 655, 660, 661, 662,
                     663, 664, 665, 666,667, 668, 669, 670, 671, 675, 677,677, 677, 678, 678, 678, 680, 681, 682, 683,
                     684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 699, 699, 700, 701, 702, 703, 704, 705,
                     706, 707, 708, 709, 710, 711, 712, 713, 714, 715,
                     39, 40, 41, 42, 646, 647, 648, 649, 652, 654, 656, 672, 673, 673, 674, 674, 676, 696, 696, 696,
                     697, 697, 698, 698]

    for t in tiles_numbers:
        if t in Tile.Tile.all:
            game.add_tile(Tile.Tile.all[t])
        else:
            print(f"OOPS tile {t}")

    game.add_paper(Misc.priority_deal())
    game.add_paper(Misc.trainyard(game, info={
        '4H': '1 operating round.\nYellow tiles.\nTrain limit: 4.\nGrey hexes: low value.',
        '6H': '2 operating rounds\nYellow and green tiles.\nTrain limit: 4.\nGrey hexes: low value.\nCompanies can buy privates.',
        '8H': '2 operating rounds\nYellow and green tiles.\nTrain limit: 3.\nGrey hexes: middle value.\n4H trains rust.',
        '10H': '3 operating rounds\nYellow, green and russet tiles.\nTrain limit: 2.\nGrey hexes: middle value.\n6H trains rust.',
        '12H': '3 operating rounds\nYellow, green and russet tiles.\nTrain limit: 2.\nGrey hexes: high value.\n'
               'Messina earthquake.',
        '16H': '3 operating rounds\nYellow, green and russet tiles.\nTrain limit: 2.\nGrey hexes: high value.\n'
               'Highest stock values available.\n8H trains rust.'
    }))

    out = Output.Output(game=game, output_file=output_file)
    out.generate()


if __name__ == '__main__':
    create_1849('1849')
