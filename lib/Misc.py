from Definitions import *
import OutputFunctions
import cairo
import Colour
import math
from math import pi
import Paper


def current_round_marker(*colours):
    width = 60*mm
    height = 60*mm
    n_circles = len(colours) + 1

    colours = [Colour.white] + list(colours)

    # surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, width, height))
    # context = cairo.Context(surface)

    paper = Paper.Paper(width, height)
    context = paper.context

    for i, colour in enumerate(colours):
        angle = -pi/2 + i * 2*pi/n_circles
        x = 30*mm + math.cos(angle) * 20*mm
        y = 30*mm + math.sin(angle) * 20*mm

        context.arc(x, y, logo_radius, 0, 2*pi)
        context.set_source_rgb(*colour.rgb)
        context.fill_preserve()
        context.set_source_rgb(*Colour.black.rgb)
        context.stroke()

        if i == 0:
            text = 'SDR'
        else:
            text = 'OR'

        OutputFunctions.draw_text(text, 'Freesans', 10, context, x, y, 'center', 'center')
        context.stroke()

    return paper


def priority_deal():
    pd = Paper.Paper()

    # pd.context.set_source_rgb(0, 0, 0)
    # pd.context.move_to(10*mm, 15*mm)
    # pd.context.show_text("Priority Deal")

    OutputFunctions.load_image('../../../graphics/misc/Elephant.png', pd.context, pd.width/2, pd.height/2,
                      pd.width-6*mm, pd.height-6*mm)

    return pd


