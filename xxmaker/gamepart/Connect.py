import math
from math import pi

import Colour
from Definitions import mm
from gamepart import City
from gamepart.Hexag import BlackTrack, WhiteTrack, DottedTrack
from graphics.cairo import Draw
from graphics.cairo.Draw import LineStyle


class Connect:
    background_width = 4*mm
    foreground_width = 3*mm

    def __init__(self, side1, side2, *args, over=False, under=False):
        self.side1 = side1
        self.side2 = side2
        self.args = args
        self.over = over
        self.under = under
        self.trackstyle = BlackTrack
        if WhiteTrack in args:
            self.trackstyle = WhiteTrack
        elif DottedTrack in args:
            self.trackstyle = DottedTrack
        self.hexag = None

    @property
    def revenuelocations(self):
        return [x for x in self.args if isinstance(x, City.RevenueLocation)]

    def draw(self, canvas, hex_location, style, draw_towns):
        towns = []
        if draw_towns:
            for arg in self.args:
                if isinstance(arg, City.Town) or isinstance(arg, City.City):
                    towns.append(arg)

        self.draw_arc(canvas, hex_location, towns, *style)

    def draw_background(self, canvas, hex_location):
        self.draw(canvas, hex_location, style=[LineStyle(Colour.white, self.background_width)],
                  draw_towns=False)

    def draw_foreground(self, canvas, hex_location):
        if self.trackstyle == WhiteTrack:
            self.draw(canvas, hex_location,
                      style=[LineStyle(Colour.black, self.foreground_width), LineStyle(Colour.white, self.foreground_width - 1*mm)],
                      draw_towns=True)
        elif self.trackstyle == DottedTrack:
            self.draw(canvas, hex_location,
                      style=[LineStyle(Colour.black, self.foreground_width), LineStyle(Colour.white, self.foreground_width - 1 * mm, dashed=True)],
                      draw_towns=True)
        else:
            self.draw(canvas, hex_location,
                      style=[LineStyle(Colour.black, self.foreground_width)],
                      draw_towns=True)

    def draw_arc(self, canvas, hex_location, towns, *styles):
        p, q = self.side1, self.side2
        xc, yc = hex_location

        h = self.hexag.unit_length
        # Create a circular arc from point P on a side of the hex to point q somehere in the hex,
        # perpendicular to the hexside at P.
        angle_origin_to_p_wrt_xaxis = math.atan2(p.y, p.x)
        # print(f"alpha = {angle_origin_to_p_wrt_xaxis}")
        angle_of_hexside_wrt_xaxis = angle_origin_to_p_wrt_xaxis - pi / 2  # plus or minus k * pi
        # print(f"beta = {angle_of_hexside_wrt_xaxis}")

        angle_of_pq_wrt_x_axis = math.atan2(q.y - p.y, q.x - p.x)
        # print(f"gamma = {angle_of_pq_wrt_x_axis}")

        while angle_of_hexside_wrt_xaxis - angle_of_pq_wrt_x_axis > pi / 2:
            angle_of_hexside_wrt_xaxis -= pi
        while angle_of_hexside_wrt_xaxis - angle_of_pq_wrt_x_axis < -pi / 2:
            angle_of_hexside_wrt_xaxis += pi

        # print(f"beta = {angle_of_hexside_wrt_xaxis}")

        pq = math.sqrt((q.x - p.x) ** 2 + (q.y - p.y) ** 2)
        # print(f"pq = {pq}")
        angle_of_pq_wrt_hexside = angle_of_pq_wrt_x_axis - angle_of_hexside_wrt_xaxis

        if abs(abs(angle_of_pq_wrt_hexside) - pi / 2) < 0.01:
            for town in towns:
                x_town = (1 - town.location) * p.x + town.location * q.x
                y_town = (1 - town.location) * p.y + town.location * q.y

                if isinstance(town, City.RevenueLocation):
                    town.x = x_town
                    town.y = y_town
                    if isinstance(town, City.Town):
                        town.angle = angle_of_pq_wrt_x_axis + pi / 2
                else:
                    Draw.line(canvas, ((x_town + town.length_bar / 2 * math.sin(angle_of_pq_wrt_x_axis)) * h + xc,
                                       (y_town - town.length_bar / 2 * math.cos(angle_of_pq_wrt_x_axis)) * h + yc),
                                      ((x_town - town.length_bar / 2 * math.sin(angle_of_pq_wrt_x_axis)) * h + xc,
                                       (y_town + town.length_bar / 2 * math.cos(angle_of_pq_wrt_x_axis)) * h + yc),
                              LineStyle(Colour.black, 3*mm))

            Draw.line(canvas, (p.x*h + xc, p.y*h + yc), (q.x*h + xc, q.y*h+yc), *styles)
        else:
            radius_of_circle = pq / (2 * abs(math.sin(angle_of_pq_wrt_x_axis - angle_origin_to_p_wrt_xaxis)))
            # print(f"radius = {radius_of_circle}")

            centre = (p.x + radius_of_circle * math.cos(angle_of_hexside_wrt_xaxis),
                      p.y + radius_of_circle * math.sin(angle_of_hexside_wrt_xaxis))

            angle_centre_to_p = math.atan2(p.y - centre[1], p.x - centre[0])
            angle_centre_to_q = math.atan2(q.y - centre[1], q.x - centre[0])

            alpha, beta = normalise_arc_angles(angle_centre_to_p, angle_centre_to_q)

            for town in towns:
                angle_town = town.location * alpha + (1 - town.location) * beta
                if True or isinstance(town, City.City):
                    x = (centre[0] + radius_of_circle * math.cos(angle_town))
                    y = (centre[1] + radius_of_circle * math.sin(angle_town))
                    town.x = x
                    town.y = y
                    if isinstance(town, City.Town):
                        town.angle = angle_town

            Draw.arc(canvas, (centre[0]*h + xc, centre[1]*h + yc), radius_of_circle*h, alpha, beta, *styles)


def normalise_arc_angles(alpha, beta):
    # Return angles equivalent to alpha and beta, appropriate for drawing
    # The return values will satisfy the conditions:
    # * The angles will be returned in ascending order
    # * One of the angles will be equal to alpha + m*pi, the other to beta + n*pi
    # * the difference between the angles is smaller than pi
    while alpha - beta > pi:
        alpha -= 2 * pi
    while beta - alpha > pi:
        beta -= 2 * pi
    return min(alpha, beta), max(alpha, beta)
