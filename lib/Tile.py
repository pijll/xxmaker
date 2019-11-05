import Colour
import cairo
from Definitions import *
from math import sqrt
from City import Town, City, DoubleCity
import Hexag
from Hexag import Connect

# Distance from flat side to flat side
tile_size = 38*mm


class Tile:
    all = {}

    def __init__(self, number, colour, *args, **kwargs):
        self.number = number
        self.colour = colour
        self.args = args

        self.hexag = Hexag.Hexag(*args, colour=colour, size=tile_size, outline=False, orientation=VERTICAL, **kwargs)

        self.surface = None
        self.context = None

        Tile.all[number] = self

    @property
    def radius(self):
        return tile_size/sqrt(3)

    @property
    def width(self):
        return 2 * self.radius

    @property
    def height(self):
        return tile_size

    def draw(self):
        if self.surface:
            return self.surface

        self.surface = self.hexag.draw()
        self.context = self.hexag.context

        self.context.set_source_rgb(*Colour.black)
        self.context.move_to(0.25 * self.hexag.side_length, 0.8 * self.hexag.side_length)
        self.context.show_text(str(self.number))

        return self.surface


SE, S, SW, NW, N, NE = Hexag.tile_sides(Hexag.VERTICAL)

# The orientation of these tiles is equal to that in the first of these games where it occurs:
# 1830 (AH), ...
Tile(1, Colour.phase_1, Connect(S, NE, Town(value=10, location=0.75, value_location=(-0.45, 0.2))),
     Connect(N, SW, Town(value=10, location=0.75, value_location=(0.45, -0.2))))   # 1830
Tile(2, Colour.phase_1, Connect(N, S, Town(value=10, location=0.25)),
     Connect(NE, SE, Town(value=10, value_location=(-0.2, 0.5))))  # 1830
Tile(3, Colour.phase_1, Connect(S, SW, Town(value=10)))     # 1830
Tile(4, Colour.phase_1, Connect(N, S, Town(value=10)))      # 1830
Tile(5, Colour.phase_1, City('A', 20), Connect(NE, 'A'), Connect("A", SE))
Tile(6, Colour.phase_1, City('A', 20), Connect(N, "A"), Connect("A", SE))
Tile(7, Colour.phase_1, Connect(S, SW))     # 1830
Tile(8, Colour.phase_1, Connect(S, NW))     # 1830
Tile(9, Colour.phase_1, Connect(N, S))      # 1830
Tile(10, Colour.phase_2, City("A", 30, -0.3, -0.6), City("B", 30, 0.3, 0.6), Connect(NW, "A"), Connect(SE, "B"))
Tile(12, Colour.phase_2, City("A", 30), Connect(S, "A"), Connect(SE, "A"), Connect(NE, "A"))
# Tile(13, Colour.phase_2, City("A", 30), Connect(N, "A"), Connect(SW, "A"), Connect(SE, "A"))
Tile(14, Colour.phase_2, Connect(N, S, DoubleCity(value=30)), Connect(NE, SW))      # 1830
Tile(15, Colour.phase_2, DoubleCity(id_="A", value=30), Connect(SW, "A"), Connect(NW, "A"),
     Connect(S, "A"), Connect(N, "A"))       # 1830
Tile(16, Colour.phase_2, Connect(SW, N, over=True), Connect(S, NW, under=True))     # 1830
Tile(17, Colour.phase_2, Connect(S, NW), Connect(N, SE))
Tile(18, Colour.phase_2, Connect(N, S), Connect(SW, NW))    # 1830
Tile(19, Colour.phase_2, Connect(S, N, under=True), Connect(NW, NE, over=True))     # 1830
Tile(20, Colour.phase_2, Connect(N, S, under=True), Connect(NW, SE, over=True))     # 1830
Tile(23, Colour.phase_2, Connect(S, N), Connect(N, SW))     # 1830
Tile(24, Colour.phase_2, Connect(S, N), Connect(S, NW))     # 1830
Tile(25, Colour.phase_2, Connect(S, NW), Connect(S, NE))    # 1830
Tile(26, Colour.phase_2, Connect(S, N), Connect(N, NW))     # 1830
Tile(27, Colour.phase_2, Connect(S, N), Connect(S, SW))     # 1830
Tile(28, Colour.phase_2, Connect(S, NW), Connect(NW, SW))   # 1830
Tile(29, Colour.phase_2, Connect(S, NW), Connect(S, SW))    # 1830
Tile(39, Colour.phase_3, Connect(S, NW), Connect(S, SW), Connect(NW, SW))   # 1830
Tile(40, Colour.phase_3, Connect(S, NW), Connect(S, NE), Connect(NW, NE))   # 1830
Tile(41, Colour.phase_3, Connect(S, N), Connect(S, SW), Connect(SW, N))     # 1830
Tile(42, Colour.phase_3, Connect(S, N), Connect(N, NW), Connect(NW, S))     # 1830
Tile(43, Colour.phase_3, Connect(S, N), Connect(S, NW, under=True), Connect(N, SW, over=True), Connect(NW, SW))     # 1830
Tile(44, Colour.phase_3, Connect(S, N, under=True), Connect(SW, NE, over=True),
     Connect(S, SW), Connect(N, NE))     # 1830
Tile(45, Colour.phase_3, Connect(S, N, under=True), Connect(S, SE), Connect(N, SW), Connect(SW, SE, over=True))     # 1830
Tile(46, Colour.phase_3, Connect(S, N, under=True), Connect(S, NW), Connect(N, NE), Connect(NW, NE, over=True))     # 1830
Tile(47, Colour.phase_3, Connect(S, N, under=True), Connect(SW, NE, over=True),
     Connect(S, NE), Connect(N, SW))     # 1830
Tile(53, Colour.phase_2, City(id_='A', value=50, value_location=(0, -.65)), Connect(S, 'A'),
     Connect(NW, 'A'), Connect(NE, 'A'), label='B')   # 1830
Tile(54, Colour.phase_2, Connect(N, NW, City(value=60)), Connect(S, SW, City(value=60)), label='NY')
Tile(55, Colour.phase_1, Connect(NW, SE, Town(value=10, location=0.25), over=True),
     Connect(S, N, Town(value=10, location=0.75), under=True))   # 1830
Tile(56, Colour.phase_1, Connect(SW, SE, Town(value=10, location=0.75), over=True),
     Connect(S, NE, Town(value=10, location=0.25)))      # 1830
Tile(57, Colour.phase_1, Connect(N, S, City(value=20)))     # 1830
Tile(58, Colour.phase_1, Connect(S, NW, Town(value=10)))    # 1830
Tile(59, Colour.phase_2, City(id_='A', value=40, x=-0.3, y=0.5), City(id_='B', value=40, x=0.3, y=-0.5, value_location=(-0.7,0)),
     Connect(S, 'A'), Connect(NE, 'B'), label='OO')   # 1830
Tile(61, Colour.phase_3, Connect(N, S, City(id_='B', value=60, value_location=(0.4, -0.7))), Connect(NW, 'B'), Connect(NE, 'B'), label='B')    # 1830
Tile(62, Colour.phase_3,DoubleCity(id_='N', value=80, x=0, y=-0.6, value_location=(-0.7, 0.6)), Connect(NW, 'N'),
     Connect(N, 'N'), DoubleCity(id_='S', value=80, x=0, y=0.6, value_location=(0.7, -0.6)),
     Connect(S, 'S'), Connect(SW, 'S'), label='NY', label_location=(0, 0))    # 1830
Tile(63, Colour.phase_3, Connect(N, S, DoubleCity(value=40)), Connect(NW, SE), Connect(NE, SW))   # 1830
Tile(64, Colour.phase_3, Connect(N, NE, City(value=50, value_location=(-0.6, -0.2))),
     Connect(S, NW, City(value=50, value_location=(0.6, 0.4))), label='OO')    # 1830
Tile(65, Colour.phase_3, Connect(SE, NE, City(value=50, value_location=(-0.3, -0.6))),
     Connect(S, NW, City(value=50, location=0.6, value_location=(-0.1,0.6))), label='OO', label_location=(-0.4,-0.6))    # 1830
Tile(66, Colour.phase_3, Connect(N, S, City(value=50, location=0.2, value_location=(0.6, 0.3))),
     Connect(SW, NW, City(value=50, value_location=(0.2, 0.6))), label='OO', label_location=(0.6, 0.2))    # 1830
Tile(67, Colour.phase_3, Connect(S, NE, City(value=50, location=0.25, value_location=(-0.3, -0.5)), over=True),
     Connect(SE, NW, City(value=50, location=0.75, value_location=(-0.1, 0.6)), under=True),
     label='OO', label_location=(-0.3,-0.8))    # 1830
Tile(68, Colour.phase_3, Connect(N, S, City(value=50, location=0.8, value_location=(-0.6, -0.15)), under=True),
     Connect(SE, NW, City(value=50, location=0.8, value_location=(+.9, -0.2)), over=True), label='OO')    # 1830
Tile(69, Colour.phase_1, Connect(S, N, Town(location=0.75, value=10), under=True),
     Connect(SW, SE, Town(location=0.75, value=10), over=True))     # 1830
Tile(70, Colour.phase_3, Connect(N, SW, under=True), Connect(S, NW, over=True), Connect(N, NW), Connect(S, SW))




