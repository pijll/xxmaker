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
    margin = 10*mm

    def __init__(self, orientation):
        self.orientation = orientation
        self.hexags = dict()
        self.game = None

    def add_hexag(self, coords, hexag=None):
        row, column = coords_to_rowcolumn(coords)
        self.hexags[row, column] = hexag or Hexag.empty
        self.hexags[row, column].map = self
        self.hexags[row, column].orientation = self.orientation

    def width_in_hexags(self):
        return max(column for row, column in self.hexags.keys())

    def height_in_hexags(self):
        return max(row for row, column in self.hexags.keys())

    def width(self):
        if self.orientation == Hexag.VERTICAL:
            return (self.width_in_hexags() * 1.5 + 1.5) * s + 2*self.margin
        else:
            return (self.width_in_hexags()/2 + 1) * hexag_size + 2*self.margin

    def height(self):
        if self.orientation == Hexag.VERTICAL:
            return (self.height_in_hexags()/2 + .5) * hexag_size + 2*self.margin
        else:
            return (self.height_in_hexags() * 1.5 + 1.5) * s + 2*self.margin

    def paper(self):
        paper = Paper.Paper(self.width(), self.height())
        for (row, column), hexag in self.hexags.items():
            x, y = self.position_of_hexag(row, column)

            paper.context.set_source_surface(hexag.draw(), int(x), y)
            paper.context.paint()

        paper.context.set_source_rgb(*Colour.black.rgb)
        Output.draw_text(self.game.name, 'Sancreek', 40, paper.context, 30, 20)
        if self.game.author:
            Output.draw_text(self.game.author, 'FreeSans', 10, paper.context, 100, 20)
        paper.context.stroke()

        return paper

    def position_of_hexag(self, row, column):
        if self.orientation == Hexag.VERTICAL:
            y = row * hexag_size / 2 + self.margin
            x = column * 1.5 * s + self.margin
        else:
            y = row * 1.5 * s + self.margin
            x = column * hexag_size / 2 + self.margin
        return x, y


def coords_to_rowcolumn(coords):
    row = row_letters.index(coords[0])
    column = int(coords[1:])
    return row, column
