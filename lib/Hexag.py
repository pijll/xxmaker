import Output
from Definitions import *
import math
from math import sqrt, pi

import cairo
import Colour
import City
import Company


hexag_size = 40*mm      # edge to edge


class Hexag:
    def __init__(self, *args, colour=None, size=None, outline=True, label=None, label_location=None,
                 orientation=None, border=None, cost=None):
        self.size = size or hexag_size
        self.surface = None
        self.context = None
        self.colour = colour or Colour.lightgreen
        self.outline = outline
        self.label = label
        self.label_location = label_location
        self.cost = cost
        self.orientation = orientation
        self.border = border

        self.revenuelocations = []
        self.connections = []
        for arg in args:
            if isinstance(arg, City.RevenueLocation):
                self.revenuelocations.append(arg)
            elif isinstance(arg, Connect):
                self.connections.append(arg)
                self.revenuelocations += arg.revenuelocations
        self.map = None

    @property
    def unit_length(self):
        return self.size/2

    @property
    def side_length(self):
        return self.size/sqrt(3)

    @property
    def width(self):
        if self.orientation == HORIZONTAL:
            return self.size
        else:
            return 2 * self.side_length

    @property
    def height(self):
        if self.orientation == VERTICAL:
            return self.size
        else:
            return 2* self.side_length

    def vertices(self):
        h = self.unit_length
        s = self.side_length
        if self.orientation == VERTICAL:
            return [(-s/2, -h), (s/2, -h), (s, 0), (s/2, h), (-s/2, h), (-s, 0)]
        else:
            return [(0, s), (h, s/2), (h, -s/2), (0, -s), (-h, -s/2), (-h, s/2)]

    def draw(self):
        if self.surface:
            return self.surface

        self.surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(-self.width, -self.height,
                                                                                         2*self.width, 2*self.height))
        self.context = cairo.Context(self.surface)
        c = self.context

        h = self.unit_length
        s = self.side_length
        vertices = self.vertices()
        c.move_to(*vertices[0])
        for v in vertices[1:]:
            c.line_to(*v)
        c.close_path()

        if self.outline:
            self.context.set_source_rgb(*self.colour)
            self.context.fill_preserve()
            self.context.set_source_rgb(*Colour.black)
            self.context.stroke()
        else:
            self.context.set_source_rgb(*self.colour)
            self.context.fill()

        city = dict()
        for ct in self.revenuelocations:
            city[ct.id] = ct

        self.context.set_source_rgb(*Colour.black)

        connections_to_draw = []
        connections_to_draw += [(conn, Colour.white, 4*mm, False) for conn in self.connections if not conn.over]
        connections_to_draw += [(conn, Colour.black, 3*mm, True) for conn in self.connections if conn.under]
        connections_to_draw += [(conn, Colour.white, 4*mm, False) for conn in self.connections if conn.over]
        connections_to_draw += [(conn, Colour.black, 3*mm, True) for conn in self.connections if not conn.under]

        for i, ct in enumerate(self.revenuelocations):
            if ct.x is None or ct.y is None:
                if len(self.revenuelocations) == 1:
                    ct.x, ct.y = 0,0
                elif len(self.revenuelocations) == 2:
                    if i == 0:
                        ct.x, ct.y = 0.6, -0.3
                    else:
                        ct.x, ct.y = -0.6, 0.3

        for conn, colour, linewidth, draw_towns in connections_to_draw:
            if isinstance(conn.side1, str):
                conn.side1 = city[conn.side1]
            if isinstance(conn.side2, str):
                conn.side2 = city[conn.side2]
            if isinstance(conn.side2, HexagEdge) and not isinstance(conn.side1, HexagEdge):
                p, q = conn.side2, conn.side1
            else:
                p, q = conn.side1, conn.side2

            towns = []
            if draw_towns:
                for arg in conn.args:
                    if isinstance(arg, City.Town) or isinstance(arg, City.City):
                        towns.append(arg)

            arc(self, p, q, towns)

            self.context.set_line_width(linewidth)
            self.context.set_source_rgb(*colour)
            self.context.stroke()

        for i, ct in enumerate(self.revenuelocations):
            ct.draw(self)
            ct.draw_name(self)
            ct.draw_value(self)

        if self.cost:
            if self.revenuelocations:
                y = -0.5 * h
            else:
                y = 0
            self.cost.draw(c, 0, y)

        if self.label:
            if self.label_location:
                x, y = self.label_location
            else:
                x, y = (0.7, 0.05)
            Output.draw_text(self.label, 'FreeSans Bold', 10, self.context, x*h, y*h, valign='center', halign='center')

        return self.surface


def arc(hexag, p, q, towns):
    context = hexag.context
    h = hexag.unit_length
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

    pq = sqrt((q.x - p.x) ** 2 + (q.y - p.y) ** 2)
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
                    town.angle = angle_of_pq_wrt_x_axis + pi/2
            else:
                context.set_line_width(3*mm)
                context.set_source_rgb(*Colour.black)
                context.move_to((x_town + town.length_bar/2 * math.sin(angle_of_pq_wrt_x_axis)) * h,
                                (y_town - town.length_bar/2 * math.cos(angle_of_pq_wrt_x_axis)) * h)
                context.line_to((x_town - town.length_bar/2 * math.sin(angle_of_pq_wrt_x_axis)) * h,
                                 (y_town + town.length_bar/2 * math.cos(angle_of_pq_wrt_x_axis)) * h)
                context.stroke()

        context.move_to(p.x * h, p.y * h)
        context.line_to(q.x * h, q.y * h)
    else:
        radius_of_circle = pq / (2 * abs(math.sin(angle_of_pq_wrt_x_axis - angle_origin_to_p_wrt_xaxis)))
        # print(f"radius = {radius_of_circle}")

        centre = (p.x + radius_of_circle * math.cos(angle_of_hexside_wrt_xaxis),
                  p.y + radius_of_circle * math.sin(angle_of_hexside_wrt_xaxis))

        angle_centre_to_p = math.atan2(p.y - centre[1], p.x - centre[0])
        angle_centre_to_q = math.atan2(q.y - centre[1], q.x - centre[0])

        alpha, beta = normalise_arc_angles(angle_centre_to_p, angle_centre_to_q)

        for town in towns:
            angle_town = town.location * alpha + (1-town.location) * beta
            if True or isinstance(town, City.City):
                x = (centre[0] + radius_of_circle * math.cos(angle_town))
                y = (centre[1] + radius_of_circle * math.sin(angle_town))
                town.x = x
                town.y = y
                if isinstance(town, City.Town):
                    town.angle = angle_town

        context.arc(centre[0] * h, centre[1] * h, radius_of_circle * h, alpha, beta)


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
    arrow_width = 0.1
    arrow_length = 0.33

    def __init__(self, *args, name=None, colour=None, links=None, values=None, value_location=None):
        self.links = links or set()
        self.name = name
        self.values = values
        self.value_location = value_location
        super().__init__(*args, colour=colour or self.default_colour)

    def draw(self):
        super().draw()
        c = self.context

        h = self.unit_length
        s = self.side_length
        for direction in self.links:
            tip_of_arrow = (direction.x * (1-self.arrow_length) * h, direction.y * (1-self.arrow_length) * h)
            left_side = ((direction.x - math.sin(direction.angle) * self.arrow_width) * h,
                         (direction.y + math.cos(direction.angle) * self.arrow_width) * h)
            right_side = ((direction.x + math.sin(direction.angle) * self.arrow_width) * h,
                          (direction.y - math.cos(direction.angle) * self.arrow_width) * h)
            self.context.move_to(*left_side)
            self.context.line_to(*tip_of_arrow)
            self.context.line_to(*right_side)
            self.context.line_to(*left_side)
            self.context.set_source_rgb(*Colour.black)
            self.context.fill()

        if self.name:
            Output.draw_text(self.name, 'FreeSans Italic', 8, c, 0, -.4*h, 'center', 'center')
            c.stroke()

        if self.values:
            if self.value_location:
                x_c, y_c = self.value_location
            else:
                x_c, y_c = 0, 0
            for i, v in enumerate(self.values):
                box_size = 8*mm
                x = (i - len(self.values)/2) * box_size + x_c * self.unit_length
                y = y_c * self.unit_length - box_size/2
                c.rectangle(x, y, box_size, box_size)
                c.set_source_rgb(*Colour.white)
                c.fill_preserve()
                c.set_source_rgb(*Colour.black)
                c.stroke()
                Output.draw_text(str(v), 'FreeSans', 8, c, x+box_size/2, y_c*self.unit_length, 'center', 'center')
                c.stroke()

        return self.surface


class LocationOnHexag:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class HexagEdge(LocationOnHexag):
    def __init__(self, angle):
        self.angle = angle
        super().__init__(x=math.cos(angle), y=math.sin(angle))


def tile_sides(orientation):
    if orientation == VERTICAL:
        start_angle = pi/6
    else:
        start_angle = 0
    for i in range(6):
        angle = start_angle + i*pi/3
        yield HexagEdge(angle=angle)


center_of_hexag = LocationOnHexag(0,0)


class Connect:
    def __init__(self, side1, side2, *args, over=False, under=False):
        self.side1 = side1
        self.side2 = side2
        self.args = args
        self.over = over
        self.under = under

    @property
    def revenuelocations(self):
        return [x for x in self.args if isinstance(x, City.RevenueLocation)]


class Cost:
    def __init__(self, cost):
        self.cost = cost


class Hill(Cost):
    def draw(self, context, x, y):
        context.move_to(x - 6 * mm, y + 0.5 * mm)
        context.line_to(x, y - 10 * mm)
        context.line_to(x + 6 * mm, y + 0.5 * mm)
        context.close_path()

        context.set_source_rgb(*Colour.brown)
        context.fill_preserve()
        context.set_source_rgb(*Colour.black)
        context.stroke()

        Output.draw_text(self.cost, 'FreeSans', 8, context, x, y, 'bottom', 'center')


class Water(Cost):
    def draw(self, context, x, y):
        context.move_to(x - 6 * mm, y + 0.5 * mm)
        context.line_to(x, y - 10 * mm)
        context.line_to(x + 6 * mm, y + 0.5 * mm)
        context.close_path()

        context.set_source_rgb(*Colour.lightblue)
        context.fill_preserve()
        context.set_source_rgb(*Colour.black)
        context.stroke()

        Output.draw_text(self.cost, 'FreeSans', 8, context, x, y, 'bottom', 'center')




empty = Hexag()
