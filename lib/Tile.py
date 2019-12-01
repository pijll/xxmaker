import Colour
import cairo
from Definitions import *
from math import sqrt
from City import Town, City, DoubleCity
import Hexag
from Hexag import Connect, WhiteTrack, DottedTrack
import OutputFunctions
import Font
import Draw
from Draw import LineStyle, FillStyle, TextStyle


# Distance from flat side to flat side
tile_size = 38*mm


class Tile:
    all = {}

    def __init__(self, number, colour, *args, **kwargs):
        self.number = number
        self.colour = colour
        self.args = args

        self.hexag = Hexag.Hexag(*args, colour=colour, size=tile_size, outline=False, orientation=VERTICAL, **kwargs)
        self.canvas = None

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
        if self.canvas:
            return self.canvas

        self.canvas = self.hexag.draw()

        Draw.text(self.canvas, (self.hexag.unit_length / (3**.5), self.hexag.unit_length), self.number,
                  TextStyle(Font.very_small, Colour.black, 'bottom', 'right'))

        return self.canvas


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
Tile(30, Colour.phase_2, Connect(S, SE), Connect(SE, N))
Tile(31, Colour.phase_2, Connect(SW, SE), Connect(SE, NE))
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
Tile(73, Colour.phase_1, Connect(SW, SE, Town(value=10), DottedTrack))
Tile(74, Colour.phase_1, Connect(NW, SE, Town(value=10), DottedTrack))
Tile(77, Colour.phase_1, Connect(NE, SE, DottedTrack))
Tile(78, Colour.phase_1, Connect(N, SE, DottedTrack))
Tile(79, Colour.phase_1, Connect(NW, SE, DottedTrack))
Tile(624, Colour.phase_2, Connect(S, SE), Connect(S, SW))
Tile(644, Colour.phase_1, City('A', value=20), Connect('A', S), Connect('A', SE, DottedTrack))
Tile(645, Colour.phase_1, City('A', value=20), Connect('A', SW), Connect('A', SE, DottedTrack))
Tile(646, Colour.phase_3, Connect(N, SW, DottedTrack), Connect(SW, SE, DottedTrack), Connect(SE, N, DottedTrack))
Tile(647, Colour.phase_3, Connect(S, SW, DottedTrack), Connect(SE, S, DottedTrack), Connect(SE, SW, DottedTrack))
Tile(648, Colour.phase_3, Connect(N, NW, DottedTrack), Connect(NW, SE, DottedTrack), Connect(SE, N, DottedTrack))
Tile(649, Colour.phase_3, Connect(NW, SW, DottedTrack), Connect(SW, SE, DottedTrack), Connect(SE, NW, DottedTrack))
Tile(650, Colour.phase_2, Connect(S, SE, DottedTrack), Connect(S, SW, DottedTrack))
Tile(651, Colour.phase_2, Connect(NW, SE, DoubleCity('A', value=90)), Connect('A', N),
     Connect('A', SW, DottedTrack), Connect('A', S, DottedTrack), label='P')
Tile(652, Colour.phase_3, Connect(NW, SE, DoubleCity('A', value=130), WhiteTrack), Connect('A', N),
     Connect('A', SW, WhiteTrack), Connect('A', S, WhiteTrack), label='P')
Tile(653, Colour.phase_2, Connect(NE, SW, City('A', value=90)), Connect('A', NW, DottedTrack), label='C')
Tile(654, Colour.phase_3, Connect(SW, NE, DoubleCity('A', value=90)),
     Connect('A', NW, WhiteTrack), Connect('A', S, WhiteTrack), label='C')
Tile(655, Colour.phase_2, DoubleCity('A', value=50), Connect('A', NW), Connect('A', NE), Connect('A', S), label='M')
Tile(656, Colour.phase_3, DoubleCity('A', value=80), Connect('A', NW), Connect('A', S),
     Connect('A', NE, WhiteTrack), Connect('A', SW, DottedTrack), label='M')
Tile(657, Colour.phase_1, City('A', value=20), Connect('A', NW), Connect('A', SE, DottedTrack))
Tile(658, Colour.phase_1, City('A', value=20), Connect('A', N), Connect('A', SE, DottedTrack))
Tile(659, Colour.phase_1, City('A', value=20), Connect('A', NE), Connect('A', SE, DottedTrack))
Tile(660, Colour.phase_2, Connect(NW, SE, DoubleCity('A', value=30)), Connect(S, N, DottedTrack))
Tile(661, Colour.phase_2, Connect(NW, SE, DoubleCity('A', value=30), DottedTrack), Connect(S, N))
Tile(662, Colour.phase_2, DoubleCity('A', value=30), Connect('A', N), Connect('A', NW),
     Connect('A', S, DottedTrack), Connect('A', SE, DottedTrack))
Tile(663, Colour.phase_2, DoubleCity('A', value=30), Connect('A', S), Connect('A', NW),
     Connect('A', N, DottedTrack), Connect('A', SE, DottedTrack))
Tile(664, Colour.phase_2, Connect(NW, SE, DoubleCity('A', value=30)), Connect(S, 'A', DottedTrack),
     Connect('A', SW, DottedTrack))
Tile(665, Colour.phase_2, Connect(NW, SE, DoubleCity('A', value=30), DottedTrack), Connect(S, 'A'), Connect('A', SW))
Tile(666, Colour.phase_2, DoubleCity('A', value=30), Connect('A', SW), Connect('A', SE),
     Connect('A', NW, DottedTrack), Connect('A', S, DottedTrack))
Tile(667, Colour.phase_2, DoubleCity('A', value=30), Connect('A', S), Connect('A', SE),
     Connect('A', NW, DottedTrack), Connect('A', SW, DottedTrack))
Tile(668, Colour.phase_2, Connect(NW, SE, DoubleCity('A', value=30)), Connect(N, 'A', DottedTrack),
     Connect('A', SW, DottedTrack))
Tile(669, Colour.phase_2, Connect(NW, SE, DoubleCity('A', value=30), DottedTrack), Connect(N, 'A'), Connect('A', SW))
Tile(670, Colour.phase_2, DoubleCity('A', value=30), Connect('A', NW), Connect('A', SW),
     Connect('A', N, DottedTrack), Connect('A', SE, DottedTrack))
Tile(671, Colour.phase_2, DoubleCity('A', value=30), Connect('A', N), Connect('A', NW),
     Connect('A', SE, DottedTrack), Connect('A', SW, DottedTrack))
Tile(672, Colour.phase_3, Connect(N, S, WhiteTrack, DoubleCity(value=40)), Connect(NW, SE, WhiteTrack))
Tile(673, Colour.phase_3, Connect(NW, SE, WhiteTrack, DoubleCity('A', value=40)), Connect('A', SW, WhiteTrack),
     Connect('A', S, WhiteTrack))
Tile(674, Colour.phase_3, Connect(NW, SE, WhiteTrack, DoubleCity('A', value=40)), Connect('A', SW, WhiteTrack),
     Connect('A', N, WhiteTrack))
Tile(675, Colour.phase_2, City('A', value=20), Connect('A', N), Connect('A', SW),
     Connect('A', NW, DottedTrack), label='S')
Tile(676, Colour.phase_3, DoubleCity('A', value=30), Connect('A', SW, WhiteTrack), Connect('A', NW, WhiteTrack),
     Connect('A', N), label='S')
Tile(677, Colour.phase_2, Connect(SE, NW, DottedTrack), Connect(SE, N, DottedTrack))
Tile(678, Colour.phase_2, Connect(SE, NW, DottedTrack), Connect(SE, SW, DottedTrack))
Tile(679, Colour.phase_1, Connect(S, SE, Town(value=10), DottedTrack))
Tile(680, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', SW),
     Connect('A', SE, DottedTrack), Connect('A', S, DottedTrack))
Tile(681, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', S),
     Connect('A', SE, DottedTrack), Connect('A', SW, DottedTrack))
Tile(682, Colour.phase_2, Town('A', value=10), Connect('A', SW), Connect('A', S),
     Connect('A', NW, DottedTrack), Connect('A', SE, DottedTrack))
Tile(683, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', SE),
     Connect('A', SW, DottedTrack), Connect('A', S, DottedTrack))
Tile(684, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', N),
     Connect('A', SE, DottedTrack), Connect('A', SW, DottedTrack))
Tile(685, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', SW),
     Connect('A', SE, DottedTrack), Connect('A', N, DottedTrack))
Tile(686, Colour.phase_2, Town('A', value=10), Connect('A', N), Connect('A', SW),
     Connect('A', SE, DottedTrack), Connect('A', NW, DottedTrack))
Tile(687, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', SE),
     Connect('A', N, DottedTrack), Connect('A', SW, DottedTrack))
Tile(688, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', S),
     Connect('A', SE, DottedTrack), Connect('A', N, DottedTrack))
Tile(689, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', N),
     Connect('A', SE, DottedTrack), Connect('A', S, DottedTrack))
Tile(690, Colour.phase_2, Town('A', value=10), Connect('A', NW), Connect('A', SE),
     Connect('A', N, DottedTrack), Connect('A', S, DottedTrack))
Tile(691, Colour.phase_2, Town('A', value=10), Connect('A', N), Connect('A', S),
     Connect('A', SE, DottedTrack), Connect('A', NW, DottedTrack))
Tile(692, Colour.phase_2, Connect(SE, NW, DottedTrack), Connect(SE, NE, DottedTrack))
Tile(693, Colour.phase_2, Connect(SE, NW, DottedTrack), Connect(SE, S, DottedTrack))
Tile(694, Colour.phase_2, Connect(SE, N, DottedTrack), Connect(SE, NE, DottedTrack))
Tile(695, Colour.phase_2, Connect(SE, SW, DottedTrack), Connect(SE, S, DottedTrack))
Tile(696, Colour.phase_3, Town('A', value=20), Connect(N, 'A', WhiteTrack), Connect(NW, 'A', WhiteTrack),
     Connect(S, 'A', WhiteTrack), Connect(SE, 'A', WhiteTrack))
Tile(697, Colour.phase_3, Town('A', value=20), Connect(SW, 'A', WhiteTrack), Connect(NW, 'A', WhiteTrack),
     Connect(S, 'A', WhiteTrack), Connect(SE, 'A', WhiteTrack))
Tile(698, Colour.phase_3, Town('A', value=20), Connect(N, 'A', WhiteTrack), Connect(NW, 'A', WhiteTrack),
     Connect(SW, 'A', WhiteTrack), Connect(SE, 'A', WhiteTrack))
Tile(699, Colour.phase_2, Connect(SE, SW, DottedTrack), Connect(SE, N, DottedTrack))
Tile(700, Colour.phase_2, Town('A', value=10), Connect('A', SW), Connect('A', SE),
     Connect('A', NW, DottedTrack), Connect('A', S, DottedTrack))
Tile(701, Colour.phase_2, Town('A', value=10), Connect('A', SE), Connect('A', S),
     Connect('A', SW, DottedTrack), Connect('A', NW, DottedTrack))
Tile(702, Colour.phase_2, Town('A', value=10), Connect('A', N), Connect('A', SE),
     Connect('A', SW, DottedTrack), Connect('A', NW, DottedTrack))
Tile(703, Colour.phase_2, Town('A', value=10), Connect('A', SW), Connect('A', SE),
     Connect('A', N, DottedTrack), Connect('A', NW, DottedTrack))
Tile(704, Colour.phase_2, DoubleCity('A', value=30), Connect('A', SW), Connect('A', SE),
     Connect('A', N, DottedTrack), Connect('A', NW, DottedTrack))
Tile(705, Colour.phase_2, DoubleCity('A', value=30), Connect('A', SE), Connect('A', N),
     Connect('A', NW, DottedTrack), Connect('A', SW, DottedTrack))
Tile(706, Colour.phase_2, DoubleCity('A', value=30), Connect('A', SW), Connect('A', NW),
     Connect('A', S, DottedTrack), Connect('A', SE, DottedTrack))
Tile(707, Colour.phase_2, DoubleCity('A', value=30), Connect('A', NW), Connect('A', S),
     Connect('A', SE, DottedTrack), Connect('A', SW, DottedTrack))
Tile(708, Colour.phase_2, Connect(SE, N, DottedTrack), Connect(SE, S, DottedTrack))
Tile(709, Colour.phase_2, Connect(SE, NE, DottedTrack), Connect(SE, SW, DottedTrack))
Tile(710, Colour.phase_2, Connect(S, NE, over=True), Connect(N, SE, DottedTrack, under=True))
Tile(711, Colour.phase_2, Connect(S, NE, under=True), Connect(SE, NW, DottedTrack, over=True))
Tile(712, Colour.phase_2, Connect(N, SE, under=True), Connect(S, NE, DottedTrack, over=True))
Tile(713, Colour.phase_2, Connect(NW, SE, over=True), Connect(S, NE, DottedTrack, under=True))
Tile(714, Colour.phase_2, Connect(NW, SE, under=True), Connect(S, N, DottedTrack, over=True))
Tile(715, Colour.phase_2, Connect(N, S, over=True), Connect(SE, NW, DottedTrack, under=True))


