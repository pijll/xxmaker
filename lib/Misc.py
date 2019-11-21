from Definitions import *
import OutputFunctions
import cairo
import Colour
import math
from math import pi
from gi.repository import Pango, PangoCairo
import Paper
import Font


class Name:
    def __init__(self, game):
        self.game = game

    def draw(self):
        surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, 50*mm, 25*mm))
        context = cairo.Context(surface)

        font = Font.game_name

        layout = PangoCairo.create_layout(context)
        layout.set_font_description(font.description)
        layout.set_text(str(self.game.name))

        ink_extent, extent_text = layout.get_extents()
        text_width, text_height = ink_extent.width / Pango.SCALE, ink_extent.height / Pango.SCALE

        surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, text_width + 10*mm, text_height + 12*mm))
        context = cairo.Context(surface)

        context.set_source_rgb(*Colour.black.rgb)
        OutputFunctions.draw_text(self.game.name, Font.game_name, context, -ink_extent.x/Pango.SCALE, -ink_extent.y/Pango.SCALE, valign='top', halign='left')
        OutputFunctions.draw_text(self.game.author, Font.game_author, context, text_width+10*mm, text_height+2*mm,
                                  valign='top', halign='right')

        return surface

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

            OutputFunctions.draw_text_old(txt, 'Freesans', 10, context, x, y, 'center', 'center')
            context.stroke()

            # arrow
            arrow_start_angle = angle + logo_radius/radius_circle + 0.15
            arrow_end_angle = angle + 2*pi/self.n_circles - logo_radius/radius_circle - 0.15
            context.arc(width/2, height/2, radius_circle, arrow_start_angle, arrow_end_angle)
            context.stroke()

            arrowhead_x = width/2 + radius_circle * math.cos(arrow_end_angle)
            arrowhead_y = height/2 + radius_circle * math.sin(arrow_end_angle)

            context.move_to(arrowhead_x, arrowhead_y)
            context.line_to(arrowhead_x + self.arrow_head_length * math.cos(arrow_end_angle - pi/2 + self.arrow_head_angle),
                            arrowhead_y + self.arrow_head_length * math.sin(arrow_end_angle - pi/2 + self.arrow_head_angle))
            context.line_to(arrowhead_x + self.arrow_head_length * math.cos(arrow_end_angle - pi/2 - self.arrow_head_angle),
                            arrowhead_y + self.arrow_head_length * math.sin(arrow_end_angle - pi/2 - self.arrow_head_angle))
            context.close_path()
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


def trainyard(game, info):
    train_papers = [train.paper() for _, train in game.trains]
    height = sum(6*mm + p.height for p in train_papers)
    width = max(100*mm + p.width for p in train_papers)

    paper = Paper.Paper(width, height)
    c = paper.context

    x = 3*mm
    y = 3*mm
    for i, train_paper in enumerate(train_papers):
        n = game.trains[i][0]

        c.set_source_rgb(*Colour.black.rgb)
        OutputFunctions.draw_text(f'{n} x', Font.Font(size=9), c, x, y, halign='left', valign='top')

        c.set_source_surface(train_paper.surface, x+10*mm, y)
        c.paint_with_alpha(0.5)

        c.set_source_rgba(1, 1, 1)
        c.set_operator(cairo.OPERATOR_HSL_COLOR)
        c.rectangle(x+10*mm, y, train_paper.width, train_paper.height)
        c.fill()

        c.set_source_rgb(*Colour.black.rgb)
        c.set_line_width(2)
        c.rectangle(x+10*mm, y, train_paper.width, train_paper.height)
        c.stroke()

        train_info = info[i]
        for j, txt in enumerate(train_info.split('\n')):
            OutputFunctions.draw_text(txt, Font.Font(size=9), c, x+10*mm+train_paper.width+5*mm, y+j*6*mm)

        y += train_paper.height + 6*mm

    return paper


