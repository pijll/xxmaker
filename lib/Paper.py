import Colour
import Font
import OutputFunctions
from Definitions import *
import Draw
from math import ceil
from Draw import LineStyle, FillStyle, TextStyle


class Paper:
    def __init__(self, width=63*mm, height=39*mm):
        self.width = width
        self.height = height

        self.canvas = Draw.Canvas((0,0), width, height)

        # self.surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, width, height))
        # self.context = cairo.Context(self.surface)
        #
        # self.font_map = PangoCairo.FontMap.get_default()

    def split_into_parts(self, max_width, max_height):
        def how_many_fit(large, small):
            return ceil(large / small)

        n_portrait_pages = how_many_fit(self.width, max_width) * how_many_fit(self.height, max_height)
        n_landscape_pages = how_many_fit(self.width, max_height) * how_many_fit(self.height, max_width)

        if n_landscape_pages < n_portrait_pages:
            split_in_parts_horizontally = how_many_fit(self.width, max_height)
            split_in_parts_vertically = how_many_fit(self.height, max_width)
        else:
            split_in_parts_horizontally = how_many_fit(self.width, max_width)
            split_in_parts_vertically = how_many_fit(self.height, max_height)

        width_map_part = self.width / split_in_parts_horizontally
        height_map_part = self.height / split_in_parts_vertically

        for column in range(split_in_parts_horizontally):
            for row in range(split_in_parts_vertically):
                paper_part = Paper(width_map_part, height_map_part)

                paper_part.canvas.draw(self.canvas, (-column * width_map_part, -row * height_map_part))
                yield paper_part


class Certificate(Paper):
    def __init__(self, colour, price=None, name=None, icon=None):
        super().__init__()
        self.colour = colour

        c = self.canvas
        Draw.rectangle(c, (0, 0), self.width, self.height, FillStyle(colour.faded()))
        Draw.rectangle(c, (3*mm, 0), 13*mm, self.height, FillStyle(colour))

        if name:
            y = self.height/2 if price else 14*mm
            OutputFunctions.draw_centered_lines(name, Font.certificate_name, c,
                                                    x_c=(self.width + 16*mm)/2, y=y,
                                                    width=self.width - 16*mm - 6*mm)

        if price:
            Draw.text(c, (self.width - 3*mm, 2.8*mm), price,
                      TextStyle(Font.price, Colour.black, 'top', 'right'))

        if icon:
            Draw.load_image(c, icon, (9.5*mm, 7*mm), width=10*mm, height=10*mm)
