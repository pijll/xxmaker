from Definitions import *
import OutputFunctions
import cairo
import Colour
import math
from math import pi
from gi.repository import Pango, PangoCairo
import Paper
import Font
import Draw
from Draw import LineStyle, FillStyle, TextStyle
from Token import Token


class Name:
    def __init__(self, game):
        self.game = game

    def draw(self):
        canvas = Draw.Canvas((0,0), 50*mm, 25*mm)
        context = canvas.context

        font = Font.game_name

        layout = PangoCairo.create_layout(context)
        layout.set_font_description(font.description)
        layout.set_text(str(self.game.name))

        ink_extent, extent_text = layout.get_extents()
        text_width, text_height = ink_extent.width / Pango.SCALE, ink_extent.height / Pango.SCALE

        canvas = Draw.Canvas((0, 0), text_width + 10*mm, text_height + 12*mm)

        Draw.text(canvas, (-ink_extent.x/Pango.SCALE, -ink_extent.y/Pango.SCALE), self.game.name,
                  TextStyle(Font.game_name, Colour.black, 'top', 'left'))
        Draw.text(canvas, (text_width+10*mm, text_height+2*mm), self.game.author,
                  TextStyle(Font.game_author, Colour.black, 'top', 'right'))

        return canvas


class RoundIndicator:
    margin = 2*mm
    minimum_space_between_circles = 10*mm

    arrow_head_angle = pi/8
    arrow_head_length = 2*mm

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

        canvas = Draw.Canvas((0,0), width, height)

        for i, (txt, colour) in enumerate(circles):
            angle = -pi/2 + i * 2*pi/self.n_circles
            x = width/2 + math.cos(angle) * radius_circle
            y = height/2 + math.sin(angle) * radius_circle

            Draw.circle(canvas, (x,y), logo_radius, FillStyle(colour), LineStyle(Colour.black, 1))
            Draw.text(canvas, (x,y), txt, TextStyle(Font.normal, Colour.black, 'exactcenter', 'exactcenter'))

            # arrow
            arrow_start_angle = angle + logo_radius/radius_circle + 0.15
            arrow_end_angle = angle + 2*pi/self.n_circles - logo_radius/radius_circle - 0.15
            Draw.arc(canvas, (width/2, height/2), radius_circle, arrow_start_angle, arrow_end_angle,
                     LineStyle(Colour.black, 0.5*mm))

            arrowhead_x = width/2 + radius_circle * math.cos(arrow_end_angle)
            arrowhead_y = height/2 + radius_circle * math.sin(arrow_end_angle)

            points = [[arrowhead_x, arrowhead_y],
                      [arrowhead_x + self.arrow_head_length * math.cos(arrow_end_angle - pi/2 + self.arrow_head_angle),
                       arrowhead_y + self.arrow_head_length * math.sin(arrow_end_angle - pi/2 + self.arrow_head_angle)],
                      [arrowhead_x + self.arrow_head_length * math.cos(arrow_end_angle - pi/2 - self.arrow_head_angle),
                       arrowhead_y + self.arrow_head_length * math.sin(arrow_end_angle - pi/2 - self.arrow_head_angle)]]
            Draw.polygon(canvas, points, LineStyle(Colour.black, 1*mm))

        return canvas


def round_indicator_token():
    return Token(image_file='misc/WingedWheel.png')


def priority_deal():
    pd = Paper.Paper()

    Draw.load_image(pd.canvas, 'misc/Elephant.png', (pd.width/2, pd.height/2),
                      pd.width-6*mm, pd.height-6*mm)

    return pd
