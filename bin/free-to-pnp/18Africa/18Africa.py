import Game
import Company
import Draw
import Train
import Misc
import Colour
import Private
import Tile
import Map
import Hexag
from Hexag import Hill, Water, Hexag as Hex, Connect
from City import City, Town, DoubleCity
import Stockmarket
from Definitions import *
import os
import Paper
import Font
import Output


license_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LICENSE.txt')
game = Game.Game(name="18Africa", author='Jeff Edmunds', license_file=license_file)

ar = Company.Company(name="Alexandria Railway", abbreviation="A",
                     colour=Colour.red, # logo='free/xxx.png',
                     n_stations=5)
aor = Company.Company(name="Algiers-Oran Railway", abbreviation="AO",
                      colour=Colour.green, # logo='free/xxx.png',
                      n_stations=2)
cgh = Company.Company(name="Cape of Good Hope & Western Railway", abbreviation="CW",
                      colour=Colour.black, # logo='free/xxx.png',
                      n_stations=3)
csa = Company.Company(name="Central South African Railway", abbreviation="CSA",
                      colour=Colour.yellow, # logo='free/xxx.png',
                      n_stations=3)
cnr = Company.Company(name="Congolese National Railway", abbreviation="CN",
                      colour=Colour.green, # logo='free/xxx.png',
                      n_stations=3)
cor = Company.Company(name="Congo-Oc\u00E9an Railway", abbreviation="CO",
                      colour=Colour.blue, # logo='free/xxx.png',
                      n_stations=4)
ear = Company.Company(name="East African Railway", abbreviation="EA",
                      colour=Colour.brown, # logo='free/xxx.png',
                      n_stations=3)
enr = Company.Company(name="Egyptian National Railway", abbreviation="EN",
                      colour=Colour.yellow, # logo='free/xxx.png',
                      n_stations=4)
kr = Company.Company(name="Kenyan Railway", abbreviation="K",
                     colour=Colour.green, # logo='free/xxx.png',
                     n_stations=3)
mfr = Company.Company(name="Marrakech-Fez Railway", abbreviation="MF",
                      colour=Colour.blue, # logo='free/xxx.png',
                      n_stations=2)
mnr = Company.Company(name="Morrocan National Railway", abbreviation="MN",
                      colour=Colour.brown, # logo='free/xxx.png',
                      n_stations=2)
nza = Company.Company(name="Nederlands Zuid African Railways", abbreviation="NZA",
                      colour=Colour.brown, # logo='free/xxx.png',
                      n_stations=3)
nr = Company.Company(name="Nigerian Railway", abbreviation="N",
                      colour=Colour.brown, # logo='free/xxx.png',
                      n_stations=2)
sr = Company.Company(name="Sudan Railway", abbreviation="S",
                      colour=Colour.blue, # logo='free/xxx.png',
                      n_stations=3)
tch = Company.Company(name="Tangier Casablanca High Speed Line", abbreviation="TC",
                      colour=Colour.yellow, # logo='free/xxx.png',
                      n_stations=2)
tor = Company.Company(name="Timbuktu-Oran Railway", abbreviation="TO",
                      colour=Colour.red, # logo='free/xxx.png',
                      n_stations=3)
ur = Company.Company(name="Ugandan Railway", abbreviation="U",
                      colour=Colour.brown, # logo='free/xxx.png',
                      n_stations=3)

game.add_company(ar, aor, cgh, csa, cnr, cor, ear, enr, kr, mfr, mnr, nza, nr, sr, tch, tor, ur)

SE, S, SW, NW, N, NE = Hexag.tile_sides(Hexag.VERTICAL)

map = Map.Map(orientation=VERTICAL, coords_inverted=True)
game.add_map(map)
map.add_hexag(coords="B9")
map.add_hexag(coords="B11", hexag=Hex(Town()))
map.add_hexag(coords="B13", hexag=Hex(Connect(N, SE, Town(value=10, name='Bissau')), colour=Colour.phase_4))

map.add_hexag(coords="C6", hexag=Hex(Town(name='Agadir')))
map.add_hexag(coords="C8")
map.add_hexag(coords="C10")
map.add_hexag(coords="C12")
map.add_hexag(coords="C14", hexag=Hex(Town(name='Lab\u00E9'), Town(name='Freetown')))

map.add_hexag(coords="D3", hexag=Hex(Connect(S, NE, City('A', name='Casablanca', value='?+20', companies=[mnr])),
                                     Connect('A', SE), colour=Colour.phase_4))
map.add_hexag(coords="D5", hexag=Hex(City(name='Marrakech', companies=[mfr])))
map.add_hexag(coords="D7")
map.add_hexag(coords="D9")
map.add_hexag(coords="D11")
map.add_hexag(coords="D13")
map.add_hexag(coords="D15")

map.add_hexag(coords="E2", hexag=Hex(Connect(SW, SE, City('A', name='Tangier', value='?+00', companies=[tch])),
                                     Connect('A', S), colour=Colour.phase_4))
map.add_hexag(coords="E4", hexag=Hex(Town(name='Mekn\u00E8s'), Town(name='Fez')))
map.add_hexag(coords="E6")
map.add_hexag(coords="E8")
map.add_hexag(coords="E10")
map.add_hexag(coords="E12", hexag=Hex(Hill(20)))
map.add_hexag(coords="E14")
map.add_hexag(coords="E16", hexag=Hex(Town(name='Abidjan')))

map.add_hexag(coords="F3", hexag=Hex(Town(name='Oran')))
map.add_hexag(coords="F5")
map.add_hexag(coords="F7")
map.add_hexag(coords="F9")
map.add_hexag(coords="F11", hexag=Hex(City(name='Timbuktu', companies=[tor])))
map.add_hexag(coords="F13")
map.add_hexag(coords="F15", hexag=Hex(Town(name='Accra')))

map.add_hexag(coords="G2", hexag=Hex(Connect(SW, NE, City(name='Algiers', value='?+20', companies=[aor])),
                                     colour=Colour.phase_4))
map.add_hexag(coords="G4")
map.add_hexag(coords="G6")
map.add_hexag(coords="G8", hexag=Hex(Hill(30)))
map.add_hexag(coords="G10")
map.add_hexag(coords="G12", hexag=Hex(Water(30)))
map.add_hexag(coords="G14", hexag=Hex(Water(50)))
map.add_hexag(coords="G16", hexag=Hex(Connect(NW, SE, City(name='Lagos', value='?+20', companies=[nr])),
                                      colour=Colour.phase_4))

map.add_hexag(coords="H1", hexag=Hex(Connect(SW, SE), colour=Colour.phase_4))
map.add_hexag(coords="H3")
map.add_hexag(coords="H5")
map.add_hexag(coords="H7", hexag=Hex(Hill(30)))
map.add_hexag(coords="H9", hexag=Hex(Hill(30)))
map.add_hexag(coords="H11")
map.add_hexag(coords="H13", hexag=Hex(Town(name='Kano')))
map.add_hexag(coords="H15", hexag=Hex(Water(50)))
map.add_hexag(coords="H17", hexag=Hex(Connect(NW, NE), colour=Colour.phase_4))
map.add_hexag(coords="H19", hexag=Hex(Connect(SE, NE, Town(name='Libreville', value=10)), colour=Colour.phase_4))

map.add_hexag(coords="I2", hexag=Hex(Connect(NW, SW, Town(name='Tunis', value=10)), colour=Colour.phase_4))
map.add_hexag(coords="I4", hexag=Hex(Town(name='Tripoli')))
map.add_hexag(coords="I6")
map.add_hexag(coords="I8")
map.add_hexag(coords="I10")
map.add_hexag(coords="I12")
map.add_hexag(coords="I14")
map.add_hexag(coords="I16")
map.add_hexag(coords="I18", hexag=Hex(Town(name='Yaounde')))
map.add_hexag(coords="I20")
map.add_hexag(coords="I22", hexag=Hex(Town(name='Louanda'), Water(80)))
map.add_hexag(coords="I24", hexag=Hex(Town(name='Lobito')))
map.add_hexag(coords="I26", hexag=Hex(Town(name='Benguela')))

map.add_hexag(coords="J5")
map.add_hexag(coords="J7")
map.add_hexag(coords="J9", hexag=Hex(Hill(30)))
map.add_hexag(coords="J11")
map.add_hexag(coords="J13", hexag=Hex(colour=Colour.phase_4))
map.add_hexag(coords="J15")
map.add_hexag(coords="J17")
map.add_hexag(coords="J19", hexag=Hex(Water(30)))
map.add_hexag(coords="J21", hexag=Hex(City(name='Brazzaville', companies=[cor]),
                                      City(name='Kinshasa', companies=[cnr]), Water(60), Colour.yellow))
map.add_hexag(coords="J23")
map.add_hexag(coords="J25")
map.add_hexag(coords="J27")
map.add_hexag(coords="J29", hexag=Hex(Town(name='Walvis Bay')))
map.add_hexag(coords="J31", hexag=Hex(Town(name='L\u00FCderitz')))
map.add_hexag(coords="J35", hexag=Hex(Connect(NE, SE), colour=Colour.phase_4))

map.add_hexag(coords="K6")
map.add_hexag(coords="K8")
map.add_hexag(coords="K10", hexag=Hex(Hill(30)))
map.add_hexag(coords="K12")
map.add_hexag(coords="K14", hexag=Hex(Town(name='Ndjamena')))
map.add_hexag(coords="K16", hexag=Hex(Town(name='Bangui')))
map.add_hexag(coords="K18", hexag=Hex(Water(30)))
map.add_hexag(coords="K20")
map.add_hexag(coords="K22")
map.add_hexag(coords="K24")
map.add_hexag(coords="K26")
map.add_hexag(coords="K28")
map.add_hexag(coords="K30")
map.add_hexag(coords="K32", hexag=Hex(Water(30)))
map.add_hexag(coords="K34")
map.add_hexag(coords="K36", hexag=Hex(Connect(NE, NW, City(name='Cape Town', value='???????', companies=[cgh])),
                                      colour=Colour.phase_4))

map.add_hexag(coords="L5", hexag=Hex(Town(name='Benghazi')))
map.add_hexag(coords="L7")
map.add_hexag(coords="L9", hexag=Hex(Town(name='Kufra')))
map.add_hexag(coords="L11")
map.add_hexag(coords="L13")
map.add_hexag(coords="L15")
map.add_hexag(coords="L17")
map.add_hexag(coords="L19", hexag=Hex(Water(30)))
map.add_hexag(coords="L21")
map.add_hexag(coords="L23")
map.add_hexag(coords="L25", hexag=Hex(Water(20)))
map.add_hexag(coords="L27", hexag=Hex(Water(30)))
map.add_hexag(coords="L29")
map.add_hexag(coords="L31", hexag=Hex(Town(name='Mafeking')))
map.add_hexag(coords="L33", hexag=Hex(Water(30)))
map.add_hexag(coords="L35")

map.add_hexag(coords="M6")
map.add_hexag(coords="M8")
map.add_hexag(coords="M10")
map.add_hexag(coords="M12")
map.add_hexag(coords="M14")
map.add_hexag(coords="M16")
map.add_hexag(coords="M18", hexag=Hex(Town(name='Wau'), Town(name='Juba')))
map.add_hexag(coords="M20", hexag=Hex(Hill(20)))
map.add_hexag(coords="M22", hexag=Hex(colour=Colour.phase_4))
map.add_hexag(coords="M24")
map.add_hexag(coords="M26", hexag=Hex(Water(30), Town(name="Lusaka")))
map.add_hexag(coords="M28", hexag=Hex(Town(name='Bulawayo')))
map.add_hexag(coords="M30")
map.add_hexag(coords="M32", hexag=Hex(City(name='Pretoria', companies=[csa]),
                                      City(name='Johannesburg', companies=[nza]), Colour.yellow))
map.add_hexag(coords="M34", hexag=Hex(Hill(30), Town(name="Port Elizabeth")))

map.add_hexag(coords='N5', hexag=Hex(City('A', name='Alexandria', value='?+30', x=-0.3, y=-0.3, companies=[ar]),
                                     Connect(SW, 'A'), Connect(S, 'A'), colour=Colour.phase_4))
map.add_hexag(coords='N7', hexag=Hex(City(name='Cairo', companies=[enr])))
map.add_hexag(coords="N9", hexag=Hex(Water(30)))
map.add_hexag(coords="N11")
map.add_hexag(coords="N13")
map.add_hexag(coords="N15", hexag=Hex(Water(30)))
map.add_hexag(coords="N17", hexag=Hex(Hill(20)))
map.add_hexag(coords="N19", hexag=Hex(colour=Colour.phase_4))
map.add_hexag(coords="N21", hexag=Hex(Connect(NW, NE), colour=Colour.phase_4))
map.add_hexag(coords="N23", hexag=Hex(Connect(S, NE), colour=Colour.phase_4))
map.add_hexag(coords="N25")
map.add_hexag(coords="N27", hexag=Hex(Water(30), Town(name="Salisbury")))
map.add_hexag(coords="N29")
map.add_hexag(coords="N31", hexag=Hex(Town(name="Louren\u00E7o Marques")))
map.add_hexag(coords="N33", hexag=Hex(Town(name='Durban')))

map.add_hexag(coords="O8", hexag=Hex(Hill(20)))
map.add_hexag(coords="O10")
map.add_hexag(coords='O12', hexag=Hex(City(name='Khartoum', companies=[sr])))
map.add_hexag(coords="O14", hexag=Hex(Water(30)))
map.add_hexag(coords="O16", hexag=Hex(Hill(30)))
map.add_hexag(coords="O18")
map.add_hexag(coords='O20', hexag=Hex(City(name='Nairobi', companies=[kr])))
map.add_hexag(coords="O22")
map.add_hexag(coords="O24", hexag=Hex(colour=Colour.phase_4))
map.add_hexag(coords="O26")
map.add_hexag(coords="O28", hexag=Hex(Town(name='Beira')))

map.add_hexag(coords="P11", hexag=Hex(Connect(NW, S, Town(name='Port Sudan', value=10)), colour=Colour.phase_4))
map.add_hexag(coords="P13", hexag=Hex(Town(name='Asmara'), Hill(30)))
map.add_hexag(coords="P15", hexag=Hex(Town(name='Addis Abeba'), Hill(30)))
map.add_hexag(coords="P17", hexag=Hex(Hill(30)))
map.add_hexag(coords="P19")
map.add_hexag(coords='P21', hexag=Hex(City(name='Mombasa', companies=[ear])))
map.add_hexag(coords="P23", hexag=Hex(Connect(N, S, City(name='Dar Es Salaam', value='?+10', companies=[ur])),
                                      colour=Colour.phase_4))
map.add_hexag(coords="P25")
map.add_hexag(coords="P27")

map.add_hexag(coords="Q14", hexag=Hex(Town(name='Djibouti')))
map.add_hexag(coords="Q16", hexag=Hex(Hill(30)))
map.add_hexag(coords="Q18")
map.add_hexag(coords="Q20", hexag=Hex(Connect(N, SW), colour=Colour.phase_4))

map.add_hexag(coords="R15", hexag=Hex(Town(name='Berbera')))
map.add_hexag(coords="R17")
map.add_hexag(coords="R19", hexag=Hex(Connect(N, NW, Town(name='Mogadishu', value=10)), colour=Colour.phase_4))


map.add_element(Misc.RoundIndicator(Colour.phase_1, Colour.phase_2, Colour.phase_3), 'bottom right')
map.add_element(Misc.Name(game), 'top right')
game.add_token(Misc.round_indicator_token())

stockmarket = [[0,5,10,22,34,45,56,58,61,64,67,71,76,82,90,100,112,126,142,160,180,205,230,255,280,300,
                320,340,360,380,400,420,440,460]]

stockmarket = Stockmarket.Stockmarket(stockmarket)
game.add_stockmarket(stockmarket)

for cell in range(9):
    stockmarket.cells[0, cell].colour = Colour.lightgreen

stockmarket.cells[0, 0].colour = Colour.black
stockmarket.cells[0, 30].colour = Colour.black

game.add_train(6, Train.Train("2", Colour.phase_1, 180, exchange_price=180,
                              text='Run between 2 cities; add all towns'))
game.add_train(4, Train.Train("3", Colour.phase_1, 300, exchange_price=180,
                              text='Run between 3 cities; add all towns'))
game.add_train(3, Train.Train("4E", Colour.phase_1, 450, exchange_price=300,
                              text='Count best 4 towns/cities; skip others'))
game.add_train(3, Train.Train("3+3", Colour.phase_1, 700, exchange_price=500,
                              text='Run between 3 cities; add towns\nDouble revenue'))
game.add_train(3, Train.Train("3+3T", Colour.phase_1, 850, exchange_price=650,
                              text='Count 3 cities, and towns between and beyond\nDouble revenue; always in recovery or boom'))
game.add_train(3, Train.Train("4+4+4E", Colour.phase_1, 1000, exchange_price=750,
                              text='Count best 4 towns/cities; skip others\nTriple revenue'))
game.add_train(3, Train.Train("4+4+4T", Colour.phase_1, 1200, exchange_price=850,
                              text='Count 4 cities, and towns between and beyond\nTriple revenue'))

government_bond = Paper.Paper()
Draw.text(government_bond.canvas, (government_bond.width/2, 10*mm), 'Government Bond 100',
          Draw.TextStyle(Font.certificate_name, Colour.black))

game.add_private(Private.Private("Cape Wine Co.", 25, 5))
game.add_private(Private.Private("Allen Rock Aggregates", 35, 5, 'Build extra yellow tile',
                                 image=''))
game.add_private(Private.Private("Thompson Wagon Works", 60, 10, 'Double upgrade in same hex'))
game.add_private(Private.Private("Jamieson Tropical Timber", 75, 12, 'One free river crossing'))
game.add_private(Private.Private("George Edmunds Colonial Factors", 115, 20, 'One free station marker'))
game.add_private(Private.Private("Madianos Olive Groves", 160, 25, 'Owner may claim Priority Deal'))

# TODO: add contracts

game.add_paper(Misc.priority_deal())
#game.add_paper(Misc.trainyard())


Tile.Tile('Af10', Colour.phase_3, Town('A', value=20), Connect(N, S), Connect(NW, SE), Connect(SW, 'A'))
Tile.Tile('Af20', Colour.phase_4, Connect(SW, SE, City(value=50, location=0.25), over=True),
          Connect(NW, S, City('A', value=50, location=0.75), under=True), Connect('A', N))
Tile.Tile('Af21', Colour.phase_4, Connect(S, NE, City(value=50, location=0.25)),
          Connect(SW, N, City('A', value=50, location=0.25)), Connect('A', NW))
Tile.Tile('Af22', Colour.phase_4, Connect(N, S), City('A', value=50, x=-0.5, y=0.3), Connect('A', N),
          Connect(S, NE, City(value=50, location=0.25)))

tiles_numbers = {1: 2, 2: 2, 3: 5, 4: 8, 6: 3, 7: 4, 8: 25, 9:30, 55:2, 56: 2, 58: 10, 69: 1, 114: 1, 115: 3,
                 10: 2, 12: 3, 13: 3, 14: 2, 15: 2, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 23: 3, 24: 3, 25: 2, 26: 2,
                 27: 2, 28: 1, 29: 1, 30: 1, 31: 1, 87: 2, 88: 2,
                 35: 2, 36: 2, 37: 2, 38: 4, 40: 1, 41: 1, 42: 1, 43: 1, 45: 1, 46: 1, 47: 1, 'Af10': 2,
                 51: 5, 169: 2, 'Af20': 1, 'Af21': 1, 'Af22': 1
}

for tile_number, count in tiles_numbers.items():
    if tile_number in Tile.Tile.all:
        for i in range(count):
            game.add_tile(Tile.Tile.all[tile_number])
    else:
        print(f"OOPS tile {tile_number}")

out = Output.Output(game=game)
out.generate()
