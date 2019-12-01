from Definitions import *
import Draw
from math import ceil


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
