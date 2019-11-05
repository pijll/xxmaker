import cairo
from Definitions import *
from gi.repository import Pango, PangoCairo
import Output


class Paper:
    def __init__(self, width=63*mm, height=39*mm):
        self.width = width
        self.height = height

        self.surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, width, height))
        self.context = cairo.Context(self.surface)

        # self.context.set_source_rgb(1, 0, 0)
        # self.context.set_line_width(0.2*mm)
        # self.context.rectangle(0, 0, width, height)
        # self.context.stroke()

        self.font_map = PangoCairo.FontMap.get_default()


def priority_deal():
    pd = Paper()

    # pd.context.set_source_rgb(0, 0, 0)
    # pd.context.move_to(10*mm, 15*mm)
    # pd.context.show_text("Priority Deal")

    Output.load_image('../../../graphics/misc/Elephant.png', pd.context, pd.width/2, pd.height/2,
                      pd.width-6*mm, pd.height-6*mm)

    return pd
