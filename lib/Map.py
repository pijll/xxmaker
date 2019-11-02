import Tile
import Hexag
import Paper
from Output import mm
import Colour
from math import sqrt
import cairo
import Output
from gi.repository import Pango, PangoCairo, fontconfig


hexag_size = Hexag.hexag_size
h = hexag_size / 2
s = hexag_size / sqrt(3)

row_letters = [char for char in ".ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


class Map:
    def __init__(self, direction):
        self.direction = direction
        self.hexags = dict()
        self.game = None

    def add_hexag(self, coords, hexag=None):
        row, column = coords_to_rowcolumn(coords)
        self.hexags[row, column] = hexag or Hexag.empty
        self.hexags[row, column].map = self

    def width_in_hexags(self):
        return max(column for row, column in self.hexags.keys())

    def height_in_hexags(self):
        return max(row for row, column in self.hexags.keys())

    def width(self):
        if self.direction == Hexag.VERTICAL:
            return (self.width_in_hexags() * 1.5 + 3.5) * s
        else:
            return 200*mm

    def height(self):
        if self.direction == Hexag.VERTICAL:
            return (self.height_in_hexags()/2 + .5) * hexag_size
        else:
            return 200*mm

    def paper(self):
        paper = Paper.Paper(self.width(), self.height())
        for (row, column), hexag in self.hexags.items():
            x, y = self.position_of_hexag(row, column)

            paper.context.set_source_surface(hexag.draw(), x, y)
            paper.context.paint()

        Output.draw_text(self.game.name, 'Sancreek', 40, paper.context, 20, 20)

        return paper

    def position_of_hexag(self, row, column):
        if self.direction == Hexag.VERTICAL:
            y = row * hexag_size / 2
            x = column * 1.5 * s
        else:
            y = row * 1.5 * s
            x = column * hexag_size / 2
        return x, y


def coords_to_rowcolumn(coords):
    row = row_letters.index(coords[0])
    column = int(coords[1:])
    return row, column
