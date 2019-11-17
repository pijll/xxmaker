from Definitions import *
import OutputFunctions
import cairo
import Colour
import math
from math import pi
import Paper


class RoundIndicator:
    margin = 2*mm
    minimum_space_between_circles = 10*mm

    def __init__(self, *phase_colours):
        self.phase_colours = phase_colours

    @property
    def circles(self):
        return [('SDR', Colour.white)] + [('OR', colour) for colour in reversed(self.phase_colours)]

    @property
    def n_circles(self):
        return len(self.phase_colours)+1

    def minimum_size(self):
        minimum_radius_circle_of_centers = self.n_circles * (2*logo_radius + self.minimum_space_between_circles)/(2*pi)
        return 2 * logo_radius + 2 * self.margin + 2*minimum_radius_circle_of_centers

    def draw(self, width=None, height=None):
        circles = self.circles

        if width is None:
            width = self.minimum_size()
        if height is None:
            height = self.minimum_size()

        radius_circle = min(width, height)/2 - self.margin - logo_radius

        surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, width, height))
        context = cairo.Context(surface)

        for i, (txt, colour) in enumerate(circles):
            angle = -pi/2 + i * 2*pi/self.n_circles
            x = width/2 + math.cos(angle) * radius_circle
            y = height/2 + math.sin(angle) * radius_circle

            context.arc(x, y, logo_radius, 0, 2*pi)
            context.set_source_rgb(*colour.rgb)
            context.fill_preserve()
            context.set_source_rgb(*Colour.black.rgb)
            context.stroke()

            OutputFunctions.draw_text(txt, 'Freesans', 10, context, x, y, 'center', 'center')
            context.stroke()

            # arrow
            arrow_start_angle = angle + logo_radius/radius_circle + 0.15
            arrow_end_angle = angle + 2*pi/self.n_circles - logo_radius/radius_circle - 0.15
            context.arc(width/2, height/2, radius_circle, arrow_start_angle, arrow_end_angle)
            context.stroke()

        return surface


def priority_deal():
    pd = Paper.Paper()

    # pd.context.set_source_rgb(0, 0, 0)
    # pd.context.move_to(10*mm, 15*mm)
    # pd.context.show_text("Priority Deal")

    OutputFunctions.load_image('../../../graphics/misc/Elephant.png', pd.context, pd.width/2, pd.height/2,
                      pd.width-6*mm, pd.height-6*mm)

    return pd


