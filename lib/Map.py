import Font
import Tile
import Hexag
import Paper
from Definitions import *
import Colour
from math import sqrt
import OutputFunctions
from Draw import LineStyle, FillStyle, TextStyle
import Draw


hexag_size = Hexag.hexag_size
h = hexag_size / 2
s = hexag_size / sqrt(3)

row_letters = [char for char in ".ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


class Map:
    margin = 10*mm

    def __init__(self, orientation, background=None, background_scale=None, background_xy=None,
                 coords_inverted=False):
        self.orientation = orientation
        self.hexags = dict()
        self.game = None
        self.elements = []
        self.background = background
        self.background_scale = background_scale
        self.background_xy = background_xy
        self.coords_inverted = coords_inverted
        self.top_row = None
        self.left_column = None

    def add_hexag(self, coords=None, row=None, column=None, hexag=None):
        hexag = hexag or Hexag.empty()
        if coords:
            row, column = self.coords_to_rowcolumn(coords)
        self.hexags[row, column] = hexag
        hexag.map = self
        hexag.orientation = self.orientation
        hexag.row = row
        hexag.column = column

        if self.top_row is None or row < self.top_row:
            self.top_row = row
        if self.left_column is None or column < self.left_column:
            self.left_column = column

    def width_in_hexags(self):
        return max(column for row, column in self.hexags.keys()) - self.left_column + 1

    def height_in_hexags(self):
        return max(row for row, column in self.hexags.keys()) - self.top_row + 1

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
        c = paper.canvas

        for (row, column), hexag in self.hexags.items():
            x, y = self.position_of_hexag(row, column)
            paper.canvas.draw(hexag.draw(), (int(x), y))

        for hexag in self.hexags.values():
            for border in hexag.borders:
                border.draw(paper.canvas)

        for private in self.game.privates:
            if private.location_on_map is None:
                continue
            if isinstance(private.location_on_map, str):
                row, column = self.coords_to_rowcolumn(private.location_on_map)
                x, y = self.position_of_hexag(row, column)
                Draw.circle(c, (x - 3*mm, y), 1*mm, LineStyle(Colour.black, 1))
                Draw.circle(c, (x + 3*mm, y), 1*mm, LineStyle(Colour.black, 1))
                Draw.line(c, (x-2*mm, y), (x+2*mm, y), LineStyle(Colour.black, 1))
                Draw.text(c, (x, y-1*mm), private.abbreviation,
                          TextStyle(Font.very_small, Colour.black, 'bottom', 'center'))

        for element, location in self.elements:
            canvas = element.draw()
            if 'top' in location:
                y = self.margin
            elif 'bottom' in location:
                y = self.height() - self.margin - canvas.height
            if 'left' in location:
                x = self.margin
            elif 'right' in location:
                x = self.width() - self.margin - canvas.width

            paper.canvas.draw(canvas, (x, y))

        # if self.background:
        #     try:
        #         image = cairo.ImageSurface.create_from_png(self.background)
        #
        #         c.save()
        #         c.scale(self.background_scale, self.background_scale)
        #         c.set_source_surface(image, *self.background_xy)
        #         c.paint_with_alpha(0.6)
        #
        #     except cairo.Error:
        #         print(f'{cairo.Error}, filename={self.background}')

        return paper

    def position_of_hexag(self, row, column):
        if self.orientation == Hexag.VERTICAL:
            y = (row - self.top_row + 1) * hexag_size / 2 + self.margin
            x = (column - self.left_column + 1) * 1.5 * s + self.margin
        else:
            y = (row - self.top_row + 1) * 1.5 * s + self.margin
            x = (column - self.left_column + 1) * hexag_size / 2 + self.margin
        return x, y

    def add_element(self, element, location='top left'):
        self.elements.append((element, location))

    def coords_to_rowcolumn(self, coords):
        row = row_letters.index(coords[0])
        column = int(coords[1:])

        if self.coords_inverted:
            return column, row
        else:
            return row, column
