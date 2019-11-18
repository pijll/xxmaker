import Tile
import Hexag
import Paper
from Definitions import *
import Colour
from math import sqrt
import cairo
import OutputFunctions
from gi.repository import Pango, PangoCairo, fontconfig


hexag_size = Hexag.hexag_size
h = hexag_size / 2
s = hexag_size / sqrt(3)

row_letters = [char for char in ".ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


class Map:
    margin = 10*mm

    def __init__(self, orientation, background=None, background_scale=None, background_xy=None):
        self.orientation = orientation
        self.hexags = dict()
        self.game = None
        self.elements = []
        self.background = background
        self.background_scale = background_scale
        self.background_xy = background_xy

    def add_hexag(self, coords=None, row=None, column=None, hexag=None):
        if coords:
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
        c = paper.context

        for (row, column), hexag in self.hexags.items():
            x, y = self.position_of_hexag(row, column)

            paper.context.set_source_surface(hexag.draw(), int(x), y)
            paper.context.paint()

        paper.context.set_source_rgb(*Colour.black.rgb)
        OutputFunctions.draw_text_old(self.game.name, 'Sancreek', 40, paper.context, 30, 20)
        if self.game.author:
            OutputFunctions.draw_text_old(self.game.author, 'FreeSans', 10, paper.context, 100, 20)
        paper.context.stroke()

        for element, location in self.elements:
            surface = element.draw()
            extents = surface.get_extents()
            if 'top' in location:
                y = self.margin
            elif 'bottom' in location:
                y = self.height() - self.margin - extents.height
            if 'left' in location:
                x = self.margin
            elif 'right' in location:
                x = self.width() - self.margin - extents.width

            paper.context.set_source_surface(surface, x, y)
            paper.context.paint()

        if self.background:
            try:
                image = cairo.ImageSurface.create_from_png(self.background)

                c.save()
                c.scale(self.background_scale, self.background_scale)
                c.set_source_surface(image, *self.background_xy)
                c.paint_with_alpha(0.6)

            except cairo.Error:
                print(f'{cairo.Error}, filename={self.background}')

        return paper

    def position_of_hexag(self, row, column):
        if self.orientation == Hexag.VERTICAL:
            y = row * hexag_size / 2 + self.margin
            x = column * 1.5 * s + self.margin
        else:
            y = row * 1.5 * s + self.margin
            x = column * hexag_size / 2 + self.margin
        return x, y

    def add_element(self, element, location='top left'):
        self.elements.append((element, location))


def coords_to_rowcolumn(coords):
    row = row_letters.index(coords[0])
    column = int(coords[1:])
    return row, column
