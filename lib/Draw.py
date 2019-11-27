import cairo
from Definitions import *


end_cap_round = object()


class LineStyle:
    def __init__(self, colour, width, dashed=False, end_cap=None):
        self.colour = colour
        self.width = width
        self.dashed = dashed
        self.end_cap = end_cap


class FillStyle:
    def __init__(self, colour):
        self.colour = colour


def _draw(context, styles):
    for i, style in enumerate(styles):
        laatste_argument = (i == len(styles) - 1)
        if isinstance(style, FillStyle):
            context.set_source_rgb(*style.colour.rgb)
            if laatste_argument:
                context.fill()
            else:
                context.fill_preserve()
        elif isinstance(style, LineStyle):
            context.set_source_rgb(*style.colour.rgb)
            context.set_line_width(style.width)
            if style.dashed or style.end_cap:
                context.save()
                context_saved = True
            else:
                context_saved = False
            if style.dashed:
                context.save()
                context.set_dash([1*mm])
            if style.end_cap == end_cap_round:
                context.set_line_cap(cairo.LineCap.ROUND)
            if laatste_argument:
                context.stroke()
            else:
                context.stroke_preserve()
            if context_saved:
               context.restore()


def line(context, start, end, *line_styles):
    """Drows a line between two points."""
    context.move_to(*start)
    context.line_to(*end)
    _draw(context, line_styles)


def polygon(context, points, *styles):
    context.move_to(*points[-1])
    for point in points:
        context.line_to(*point)
    context.close_path()

    _draw(context, styles)


def circle(context, center, radius, *styles):
    context.arc(*center, radius, 0, 2*3.142)
    _draw(context, styles)


def arc(context, center, radius, angle_start, angle_end, *styles):
    context.arc(*center, radius, angle_start, angle_end)
    _draw(context, styles)


def triangle(context, center, side_length, *styles):
    """Draw an upright equilateral triangle."""
    height = 3**.5 / 2 * side_length
    points = [(center[0] + x, center[1] + y)
              for x,y in [(0, -height*2/3), (+side_length/2, height/3), (-side_length/2, height/3)]]
    polygon(context, points, *styles)


def rectangle(context, corner, width, height, *styles):
    x, y = corner
    points = [(x, y), (x+width, y), (x+width, y+height), (x, y+height)]
    polygon(context, points, *styles)
