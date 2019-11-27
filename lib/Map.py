import Font
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
        hexag = hexag or Hexag.empty()
        if coords:
            row, column = coords_to_rowcolumn(coords)
        self.hexags[row, column] = hexag
        hexag.map = self
        hexag.orientation = self.orientation
        hexag.row = row
        hexag.column = column

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

        for hexag in self.hexags.values():
            for border in hexag.borders:
                border.draw(paper.context)

        for private in self.game.privates:
            if private.location_on_map is None:
                continue
            if isinstance(private.location_on_map, str):
                row, column = coords_to_rowcolumn(private.location_on_map)
                x, y = self.position_of_hexag(row, column)
                c.set_line_width(1)
                c.set_source_rgb(*Colour.black.rgb)
                c.arc(x - 3*mm, y, 1*mm, 0, 6.29)
                c.stroke()
                c.arc(x + 3*mm, y, 1*mm, 0, 6.29)
                c.move_to(x-2*mm, y)
                c.line_to(x+2*mm, y)
                c.stroke()

                OutputFunctions.draw_text(private.abbreviation, Font.very_small, c, x, y-1*mm, 'bottom', 'center')
                c.stroke()

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
