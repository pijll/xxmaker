
# License:
# I give permission for anyone to design and post components for 1800 on boardgamegeek.
# I am very pleased with what has been done so far. I also give permission for anyone to
# download my files and make games for themselves. If someone wishes to produce some sets
# and distribute them, it is OK with me provided that the total price is for materials
# and postage only- no profit or "handling". I hope that players will use 1800 as an
# introduction to the great 18xx series of games. Antonio Leal
# https://boardgamegeek.com/thread/1785984/permission-granted


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


game = Game.Game(name="1800")

map = Map.Map(direction=Hexag.VERTICAL)
game.add_map(map)
map.add_hexag(coords="A3", hexag=Hexag.External(City(), links={"S"}))
map.add_hexag(coords="C3", hexag=Hexag.Hexag(text="$50"))
map.add_hexag(coords="D2", hexag=Hexag.Hexag(Town()))
map.add_hexag(coords="D4", hexag=Hexag.Hexag(Town()))
map.add_hexag(coords="E1", hexag=Hexag.Hexag(City(companies=["DR"])))
map.add_hexag(coords="E3", hexag=Hexag.Hexag(City(x=-0.5), City(x=0.5), colour=Colour.phase_1))
map.add_hexag(coords="E5", hexag=Hexag.Hexag(City(companies=["CS"])))
map.add_hexag(coords="F2", hexag=Hexag.Hexag(text="$40"))
map.add_hexag(coords="F4", hexag=Hexag.Hexag(text="$40"))
map.add_hexag(coords="G1", hexag=Hexag.External(links={"N"}))
map.add_hexag(coords="G3", hexag=Hexag.Hexag(City(y=0.4), text="$40"))
map.add_hexag(coords="G5", hexag=Hexag.External(links={"N"}))
map.add_hexag(coords="H2", hexag=Hexag.External(links={"SE"}))
map.add_hexag(coords="H4", hexag=Hexag.External(links={"SW"}))
map.add_hexag(coords="I3", hexag=Hexag.Hexag(City(companies=["CM"])))

stockmarket = [
    [100, 110, 120, 130],
    [90, 100, 110],
    [80, 90, 100],
    [None, 80]
]

stockmarket = Stockmarket.Stockmarket(stockmarket)
game.add_stockmarket(stockmarket)

company1 = Company.Company(name="Colorado and Southern", abbreviation="CS",
                           colour=(0, 1, 0), logo='free/Colorado_and_Southern.png',
                           n_stations=12)
company2 = Company.Company(name="Denver and Rio Grande Western", abbreviation="DR",
                           colour=(1, 0, 0), logo='free/Denver_Rio_Grande.png',
                           n_stations=12)

# The Colorado & Western does not seem to be a historical company.
# I've replaced it with the Colorado Midland, based in Colorado Springs
company3 = Company.Company(name="Colorado Midland", abbreviation="CM",
                           colour=(0, 0, 1), logo='free/Colorado_Midland.png',
                           n_stations=12)

game.add_company(company1)
game.add_company(company2)
game.add_company(company3)

train_icon = 'icons/TrafficSignDE.png'

game.add_train(3, Train.Train("2", Colour.phase_1, "$180", rusted_by='4', image=train_icon))
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

tiles_numbers = [3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 12, 12, 16, 18, 19, 23, 24, 25, 26, 27, 28, 29,
                 39, 40, 41, 42, 43, 45, 46, 58, 58, 59, 64, 65, 67, 68, 70, 800, 802, 803, 804, 805, 806, 807, 808,
                 5, 6, 12, 15, 802, 804]

for t in tiles_numbers:
    if t in Tile.Tile.all:
        game.add_tile(Tile.Tile.all[t])
    else:
        print(f"OOPS tile {t}")


out = Output.Output(game=game)
out.generate()
