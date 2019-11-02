import Colour
import cairo
from Output import mm
from math import sqrt
from City import Town, City, DoubleCity
import Hexag
from Hexag import Connect

# Distance from flat side to flat side
tile_size = 38*mm


class Tile:
    all = {}

    def __init__(self, number, colour, *args):
        self.number = number
        self.colour = colour
        self.args = args

        self.hexag = Hexag.Hexag(*args, colour=colour, size=tile_size, outline=False)

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
        self.context.move_to(0.35*self.hexag.radius, 0.8*self.hexag.radius)
        self.context.show_text(str(self.number))

        return self.surface


town = Town()

N,S,NW,NE,SW,SE = "N", "S", "NW", "NE", "SW", "SE"

# These tiles use the tile database from 18xx.info for their orientation.
Tile(1, Colour.phase_1, Connect(S, NW, Town(location=0.25)), Connect(N, SE, Town(location=0.25)))
Tile(2, Colour.phase_1, Connect(SE, NW, Town(location=0.25)), Connect(N, NE, town))
Tile(3, Colour.phase_1, Connect(S, SE, town))
Tile(4, Colour.phase_1, Connect(NW, SE, town))
Tile(5, Colour.phase_1, City("A"), Connect(NE, "A"), Connect("A", SE))
Tile(6, Colour.phase_1, City("A"), Connect(N, "A"), Connect("A", SE))
Tile(7, Colour.phase_1, Connect(SE, NE)),
Tile(8, Colour.phase_1, Connect(N, SE)),
Tile(9, Colour.phase_1, Connect(NW, SE))
Tile(10, Colour.phase_2, City("A", 30, -0.3, -0.6), City("B", 30, 0.3, 0.6), Connect(NW, "A"), Connect(SE, "B"))
Tile(12, Colour.phase_2, City("A", 30), Connect(S, "A"), Connect(SE, "A"), Connect(NE, "A"))
Tile(13, Colour.phase_2, City("A", 30), Connect(N, "A"), Connect(SW, "A"), Connect(SE, "A"))
Tile(14, Colour.phase_2, DoubleCity("A", 30), Connect(N, "A"), Connect(NW, "A"), Connect(S, "A"), Connect(SE, "A"))
Tile(15, Colour.phase_2, DoubleCity("A", 30), Connect(SW, "A"), Connect(NW, "A"), Connect(S, "A"), Connect(SE, "A"))
Tile(16, Colour.phase_2, Connect(S, NE, over=True), Connect(N, SE, under=True))
Tile(17, Colour.phase_2, Connect(S, NW), Connect(N, SE))
Tile(18, Colour.phase_2, Connect(NW, SE), Connect(SW, S))
Tile(19, Colour.phase_2, Connect(S, NE, under=True), Connect(NW, SE, over=True))
Tile(20, Colour.phase_2, Connect(N, S, under=True), Connect(NW, SE, over=True))
Tile(23, Colour.phase_2, Connect(SE, NW), Connect(N, SE))
Tile(24, Colour.phase_2, Connect(SE, NW), Connect(SW, SE))
Tile(25, Colour.phase_2, Connect(SE, SW), Connect(SE, N))
Tile(26, Colour.phase_2, Connect(SE, NW), Connect(SE, NE))
Tile(27, Colour.phase_2, Connect("S", "N"), Connect("S", "SW"))
Tile(28, Colour.phase_2, Connect("S", "NE"), Connect("S", "SE"))
Tile(29, Colour.phase_2, Connect("S", "NW"), Connect("S", "SW"))
Tile(39, Colour.phase_3, Connect("S", "NE"), Connect("S", "SE"), Connect("NE", "SE"))
Tile(40, Colour.phase_3, Connect("S", "NW"), Connect("S", "NE"), Connect("NW", "NE"))
Tile(41, Colour.phase_3, Connect("S", "N"), Connect("S", "SW"), Connect("SW", "N"))
Tile(42, Colour.phase_3, Connect("S", "N"), Connect("S", "SE"), Connect("SE", "N"))
Tile(43, Colour.phase_3, Connect("S", "N"), Connect("S", "NW", under=True), Connect("N", "SW", over=True), Connect("NW", "SW"))
Tile(45, Colour.phase_3, Connect("S", "N", under=True), Connect("S", "NE"), Connect("N", "NW"), Connect("NW", "NE", over=True))
Tile(46, Colour.phase_3, Connect("S", "N", under=True), Connect("S", "NW"), Connect("N", "NE"), Connect("NW", "NE", over=True))
Tile(55, Colour.phase_1, Connect(NW, SE, Town(location=0.25)), Connect(SW, NE, Town(location=0.75)))
Tile(56, Colour.phase_1, Connect(N, SE, Town(location=0.25)), Connect(S, NE, Town(location=0.75)))
Tile(57, Colour.phase_1, City("A"), Connect(NW, SE))
Tile(58, Colour.phase_1, Connect(SW, SE, Town()))
Tile(59, Colour.phase_2, City("A", 30, 0, -0.4), City("B", 30, -0.3, 0.5), Connect("N", "A"), Connect("SE", "B"))
Tile(64, Colour.phase_3, City("A", 40, 0.3, -0.4), City("B", 40, -0.1, 0.5), Connect("N", "A"), Connect("NE", "A"), Connect("S", "B"), Connect("NW", "B"))
Tile(65, Colour.phase_3, City("A", 40, -0.4, -0.2), City("B", 40, 0.6, 0), Connect("S", "A"), Connect("NW", "A"), Connect("NE", "B"), Connect("SE", "B"))
Tile(67, Colour.phase_3, City("A", 40, -0.4, -0.2), City("B", 40, 0.5, -0.3), Connect("S", "A", over=True), Connect("NW", "A"), Connect("SW", "B", under=True), Connect("NE", "B"))
Tile(68, Colour.phase_3, City("A", 40, 0, 0.55), City("B", 40, 0.5, -0.3), Connect("N", "A", under=True), Connect("S", "A"), Connect("SW", "B", over=True), Connect("NE", "B"))
Tile(69, Colour.phase_1, Connect(NW, SE, Town(location=0.25)), Connect(S, NE, Town(location=0.75)))
Tile(70, Colour.phase_3, Connect("N", "SW", under=True), Connect("S", "NW", over=True), Connect("N", "NW"), Connect("S", "SW"))




