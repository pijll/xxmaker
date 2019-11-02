import Output
from Output import mm
import math
from math import sqrt, pi

import cairo
import Colour
import City
import Company


hexag_size = 40*mm      # edge to edge
HORIZONTAL = object()
VERTICAL = object()

class Hexag:
    def __init__(self, *args, colour=None, size=None, outline=True, text=None):
        self.size = size or hexag_size
        self.surface = None
        self.context = None
        self.colour = colour or Colour.lightgreen
        self.outline = outline
        self.text = text

        self.cities = []
        self.connections = []
        for arg in args:
            if isinstance(arg, City.City):
                self.cities.append(arg)
            elif isinstance(arg, Connect):
                self.connections.append(arg)
        self.map = None

    @property
    def radius(self):
        return self.size/sqrt(3)

    @property
    def width(self):
        return 2 * self.radius

    @property
    def height(self):
        return self.size

    def draw(self):
        if self.surface:
            return self.surface

        self.surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(-self.width, -self.height,
                                                                                         2*self.width, 2*self.height))
        self.context = cairo.Context(self.surface)

        h = self.height/2
        s = self.radius
        point = {
            'C': (0, 0),    # centre
            '1': (-s/2, -h),  # vertices
            '2': (s/2, -h),
            '3': (s, 0),
            '4': (s/2, h),
            '5': (-s/2, h),
            '6': (-s, 0),
            'N': (0, -h),
            'NE': (3/4*s, -h/2),
            'SE': (3/4*s, h/2),
            'S': (0, h),
            'SW': (-3/4*s, h/2),
            'NW': (-3/4*s, -h/2)
        }

        self.context.move_to(*point['1'])
        self.context.line_to(*point['2'])
        self.context.line_to(*point['3'])
        self.context.line_to(*point['4'])
        self.context.line_to(*point['5'])
        self.context.line_to(*point['6'])
        self.context.line_to(*point['1'])

        if self.outline:
            self.context.set_source_rgb(*self.colour)
            self.context.fill_preserve()
            self.context.set_source_rgb(*Colour.black)
            self.context.stroke()
        else:
            self.context.set_source_rgb(*self.colour)
            self.context.fill()

        for city in self.cities:
            point[city.id] = city.x * self.size/2, city.y * self.size/2

        self.context.set_source_rgb(*Colour.black)

        connections_to_draw = []
        connections_to_draw += [(conn, Colour.white, 4*mm, False) for conn in self.connections if not conn.over]
        connections_to_draw += [(conn, Colour.black, 3*mm, True) for conn in self.connections if conn.under]
        connections_to_draw += [(conn, Colour.white, 4*mm, False) for conn in self.connections if conn.over]
        connections_to_draw += [(conn, Colour.black, 3*mm, True) for conn in self.connections if not conn.under]

        for conn, colour, linewidth, draw_towns in connections_to_draw:
            if conn.side1 in ('N', 'NW', 'NE', 'S', 'SW', 'SE'):
                p, q = point[conn.side1], point[conn.side2]
            else:
                p, q = point[conn.side2], point[conn.side1]

            towns = []
            if draw_towns:
                for arg in conn.args:
                    if isinstance(arg, City.Town):
                        towns.append(arg)

            arc(self.context, p, q, towns)

            self.context.set_line_width(linewidth)
            self.context.set_source_rgb(*colour)
            self.context.stroke()

        for city in self.cities:
            self.context.set_source_rgb(*Colour.white)
            x = city.x * self.size/2
            y = city.y * self.size/2
            city.draw(self.map, self.context, x, y)

        if self.text:
            Output.draw_text(self.text, 'FreeSans', 8, self.context, 0, -0.3*h, halign='center')

        return self.surface


def arc(context, p, q, towns):
    # Create a circular arc from point P on a side of the hex to point q somehere in the hex,
    # perpendicular to the hexside at P.
    angle_origin_to_p_wrt_xaxis = math.atan2(p[1], p[0])
    # print(f"alpha = {angle_origin_to_p_wrt_xaxis}")
    angle_of_hexside_wrt_xaxis = angle_origin_to_p_wrt_xaxis - pi / 2  # plus or minus k * pi
    # print(f"beta = {angle_of_hexside_wrt_xaxis}")

    angle_of_pq_wrt_x_axis = math.atan2(q[1] - p[1], q[0] - p[0])
    # print(f"gamma = {angle_of_pq_wrt_x_axis}")

    while angle_of_hexside_wrt_xaxis - angle_of_pq_wrt_x_axis > pi / 2:
        angle_of_hexside_wrt_xaxis -= pi
    while angle_of_hexside_wrt_xaxis - angle_of_pq_wrt_x_axis < -pi / 2:
        angle_of_hexside_wrt_xaxis += pi

    # print(f"beta = {angle_of_hexside_wrt_xaxis}")

    pq = sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
    # print(f"pq = {pq}")
    angle_of_pq_wrt_hexside = angle_of_pq_wrt_x_axis - angle_of_hexside_wrt_xaxis

    if abs(abs(angle_of_pq_wrt_hexside) - pi / 2) < 0.01:
        for town in towns:
            x_town = (1 - town.location) * p[0] + town.location * q[0]
            y_town = (1 - town.location) * p[1] + town.location * q[1]

            context.set_line_width(3*mm)
            context.set_source_rgb(*Colour.black)
            # context.arc(x_town, y_town, 5*mm, 0, 2*pi)
            context.move_to(x_town + town.length_bar/2 * math.sin(angle_of_pq_wrt_x_axis),
                            y_town - town.length_bar/2 * math.cos(angle_of_pq_wrt_x_axis))
            context.line_to(x_town - town.length_bar/2 * math.sin(angle_of_pq_wrt_x_axis),
                            y_town + town.length_bar/2 * math.cos(angle_of_pq_wrt_x_axis))
            context.stroke()

        context.move_to(*p)
        context.line_to(*q)
    else:
        radius_of_circle = pq / (2 * abs(math.sin(angle_of_pq_wrt_x_axis - angle_origin_to_p_wrt_xaxis)))
        # print(f"radius = {radius_of_circle}")

        centre = (p[0] + radius_of_circle * math.cos(angle_of_hexside_wrt_xaxis),
                  p[1] + radius_of_circle * math.sin(angle_of_hexside_wrt_xaxis))

        angle_centre_to_p = math.atan2(p[1] - centre[1], p[0] - centre[0])
        angle_centre_to_q = math.atan2(q[1] - centre[1], q[0] - centre[0])

        alpha, beta = normalise_arc_angles(angle_centre_to_p, angle_centre_to_q)

        for town in towns:
            angle_town = town.location * alpha + (1-town.location) * beta
            context.move_to(centre[0] + (radius_of_circle-town.length_bar/2) * math.cos(angle_town),
                            centre[1] + (radius_of_circle-town.length_bar/2) * math.sin(angle_town))
            context.line_to(centre[0] + (radius_of_circle+town.length_bar/2) * math.cos(angle_town),
                            centre[1] + (radius_of_circle+town.length_bar/2) * math.sin(angle_town))
            context.set_line_width(3*mm)
            context.set_source_rgb(*Colour.black)
            context.stroke()

        context.arc(centre[0], centre[1], radius_of_circle, alpha, beta)


def normalise_arc_angles(alpha, beta):
    # Return angles equivalent to alpha and beta, appropriate for drawing
    # The return values will satisfy the conditions:
    # * The angles will be returned in ascending order
    # * One of the angles will be equal to alpha + m*pi, the other to beta + n*pi
    # * the difference betwee the angles is smaller than pi
    while alpha - beta > pi:
        alpha -= 2*pi
    while beta - alpha > pi:
        beta -= 2*pi
    return min(alpha, beta), max(alpha, beta)


class External(Hexag):
    default_colour = Colour.red
    arrow_width = 0.2
    arrow_length = 0.3

    def __init__(self, *args, colour=None, links=None):
        self.links = links or set()
        super().__init__(*args, colour=colour or self.default_colour)

    def draw(self):
        super().draw()

        h = self.height/2
        s = self.radius
        for direction in self.links:
            if direction == 'S':
                self.context.move_to(-self.arrow_width*h/2, h)
                self.context.line_to(0, (1-self.arrow_length)*h)
                self.context.line_to(self.arrow_width*h/2, h)
                self.context.close_path()
            elif direction == 'N':
                self.context.move_to(-self.arrow_width*h/2, -h)
                self.context.line_to(0, -(1-self.arrow_length)*h)
                self.context.line_to(self.arrow_width*h/2, -h)
                self.context.close_path()
            elif direction == 'SW':
                self.context.move_to(-0.75*s - self.arrow_width/4*h, (0.5 - self.arrow_width*sqrt(3)/4)*h)
                self.context.line_to(-0.75*s + self.arrow_length*sqrt(3)/2*h, (0.5 - self.arrow_length/2)*h)
                self.context.line_to(-0.75*s + self.arrow_width/4*h, (0.5 + self.arrow_width*sqrt(3)/4)*h)
                self.context.close_path()
            elif direction == 'SE':
                self.context.move_to(0.75*s + self.arrow_width/4*h, (0.5 - self.arrow_width*sqrt(3)/4)*h)
                self.context.line_to(0.75*s - self.arrow_length*sqrt(3)/2*h, (0.5 - self.arrow_length/2)*h)
                self.context.line_to(0.75*s - self.arrow_width/4*h, (0.5 + self.arrow_width*sqrt(3)/4)*h)
                self.context.close_path()
            elif direction == 'NW':
                self.context.move_to(-0.75*s - self.arrow_width/4*h, -(0.5 - self.arrow_width*sqrt(3)/4)*h)
                self.context.line_to(-0.75*s + self.arrow_length*sqrt(3)/2*h, -(0.5 - self.arrow_length/2)*h)
                self.context.line_to(-0.75*s + self.arrow_width/4*h, -(0.5 + self.arrow_width*sqrt(3)/4)*h)
                self.context.close_path()
            elif direction == 'NE':
                self.context.move_to(0.75*s + self.arrow_width/4*h, -(0.5 - self.arrow_width*sqrt(3)/4)*h)
                self.context.line_to(0.75*s - self.arrow_length*sqrt(3)/2*h, -(0.5 - self.arrow_length/2)*h)
                self.context.line_to(0.75*s - self.arrow_width/4*h, -(0.5 + self.arrow_width*sqrt(3)/4)*h)
                self.context.close_path()
            self.context.set_source_rgb(*Colour.black)
            self.context.fill()

        return self.surface


class HexagEdge:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def tile_sides(orientation):
    if orientation == HORIZONTAL:
        start_angle = pi/6
    else:
        start_angle = 0
    for i in range(6):
        angle = start_angle - i*pi/3
        return HexagEdge(math.cos(angle), math.sin(angle))


class Connect:
    def __init__(self, side1, side2, *args, over=False, under=False):
        self.side1 = side1
        self.side2 = side2
        self.args = args
        self.over = over
        self.under = under


empty = Hexag()
