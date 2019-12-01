import cairo
from Definitions import *
from gi.repository import Pango, PangoCairo
import Draw


class Paper:
    def __init__(self, width=63*mm, height=39*mm):
        self.width = width
        self.height = height

        self.canvas = Draw.Canvas((0,0), width, height)

        # self.surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, width, height))
        # self.context = cairo.Context(self.surface)
        #
        # self.font_map = PangoCairo.FontMap.get_default()
