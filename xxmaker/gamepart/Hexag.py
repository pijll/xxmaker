from Definitions import *
import math
from math import sqrt, pi

import Colour
from . import City
import Font
from graphics.cairo import Draw
from graphics.cairo.Draw import LineStyle, FillStyle, TextStyle


hexag_size = 40 * mm  # edge to edge


class Hexag:
    def __init__(self, *args, colour=None, size=None, outline=True, label=None, label_location=None,
                 orientation=None, cost=None, no_border=None, row=None, column=None, icon=None):
        self.size = size or hexag_size
        self.canvas = None
        self.colour = colour or Colour.background
        self.outline = outline
        self.label = Label(label, label_location) if label is not None else None
        self.cost = cost
        self.orientation = orientation
        self.no_border = no_border or []
        self.row = row
        self.column = column
        self.icon = icon

        self.revenuelocations = []
        self.connections = []
        self.borders = []
        for arg in args:
            if isinstance(arg, City.RevenueLocation):
                self.revenuelocations.append(arg)
            elif isinstance(arg, Connect):
                self.connections.append(arg)
                self.revenuelocations += arg.revenuelocations
            elif isinstance(arg, Cost):
                self.cost = arg
            elif isinstance(arg, Colour.Colour):
                self.colour = arg
            elif isinstance(arg, Border):
                self.borders.append(arg)
                arg.hexag = self
            elif isinstance(arg, Label):
                self.label = arg

        self.map = None

    @property
    def unit_length(self):
        return self.size / 2

    @property
    def side_length(self):
        return self.size / sqrt(3)

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
            return 2 * self.side_length

    def location_on_map(self):
        return self.map.position_of_hexag(self.row, self.column)

    def vertices(self):
        if self.orientation == VERTICAL:
            start_angle = 0
        else:
            start_angle = pi/6
        return [Vertex(angle=start_angle + x * pi/3) for x in range(6)]

    def draw(self):
        if self.canvas:
            return self.canvas

        self.canvas = Draw.Canvas((-self.width, -self.height), 2 * self.width, 2 * self.height)
        c = self.canvas

        h = self.unit_length

        if self.colour != Colour.transparent:
            vertices = self.vertices()
            points = [v.xy(unit_length=self.unit_length) for v in vertices]
            Draw.polygon(c, points, FillStyle(colour=self.colour))

        city = dict()
        for ct in self.revenuelocations:
            city[ct.id] = ct

        connections_to_draw = []
        connections_to_draw += [(conn, Colour.white, 4 * mm, False) for conn in self.connections if not conn.over]
        connections_to_draw += [(conn, Colour.black, 3 * mm, True) for conn in self.connections if conn.under]
        connections_to_draw += [(conn, Colour.white, 4 * mm, False) for conn in self.connections if conn.over]
        connections_to_draw += [(conn, Colour.black, 3 * mm, True) for conn in self.connections if not conn.under]

        for i, ct in enumerate(self.revenuelocations):
            if ct.x is None or ct.y is None:
                if len(self.revenuelocations) == 1:
                    ct.x, ct.y = 0, 0
                elif len(self.revenuelocations) == 2:
                    if self.orientation == HORIZONTAL:
                        ct.x, ct.y = 0.6, -0.3
                    else:
                        ct.x, ct.y = 0.45, -0.3
                    if i == 1:
                        ct.x, ct.y = -ct.x, -ct.y

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

            if colour == Colour.black and conn.trackstyle == WhiteTrack:
                draw_arc(self, p, q, towns, LineStyle(colour, linewidth), LineStyle(Colour.white, linewidth-1*mm))
            elif colour == Colour.black and conn.trackstyle == DottedTrack:
                draw_arc(self, p, q, towns, LineStyle(colour, linewidth),
                         LineStyle(Colour.white, linewidth-1*mm, dashed=True))
            else:
                draw_arc(self, p, q, towns, LineStyle(colour, linewidth))

        for i, ct in enumerate(self.revenuelocations):
            ct.draw(self)
            ct.draw_name(self)
            ct.draw_value(self)

        if self.cost:
            if self.revenuelocations:
                y = - self.revenuelocations[0].name_distance * h - 3 * mm
            else:
                y = 0
            self.cost.draw(c, 0, y)

        if self.label:
            if self.label.location:
                x, y = self.label.location
            else:
                # x, y = (0.7, 0.05)
                x, y = (-0.5, -0.75)
            Draw.text(self.canvas, (x*h, y*h), self.label.text, TextStyle(Font.label, Colour.black, 'center', 'left'))

        if self.icon:
            self.canvas.draw(self.icon, (-0.5, 0.4))

        if self.outline:
            hex_edges = list(tile_sides(self.orientation))
            for hex_edge in hex_edges:
                if hex_edge not in self.no_border:
                    xy_start = hex_edge.left_vertex.xy(unit_length=self.unit_length)
                    xy_end = hex_edge.right_vertex.xy(unit_length=self.unit_length)
                    Draw.line(self.canvas, xy_start, xy_end, LineStyle(Colour.black, 1))

        return self.canvas


def draw_arc(hexag, p, q, towns, *styles):
    canvas = hexag.canvas
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
                    town.angle = angle_of_pq_wrt_x_axis + pi / 2
            else:
                Draw.line(canvas, ((x_town + town.length_bar / 2 * math.sin(angle_of_pq_wrt_x_axis)) * h,
                                   (y_town - town.length_bar / 2 * math.cos(angle_of_pq_wrt_x_axis)) * h),
                                  ((x_town - town.length_bar / 2 * math.sin(angle_of_pq_wrt_x_axis)) * h,
                                   (y_town + town.length_bar / 2 * math.cos(angle_of_pq_wrt_x_axis)) * h),
                          LineStyle(Colour.black, 3*mm))

        Draw.line(canvas, (p.x*h, p.y*h), (q.x*h, q.y*h), *styles)
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

        Draw.arc(canvas, (centre[0]*h, centre[1]*h), radius_of_circle*h, alpha, beta, *styles)


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


class External(Hexag):
    default_colour = Colour.red
    arrow_width = 0.1
    arrow_length = 0.4

    def __init__(self, *args, name=None, colour=None, links=None, values=None, value_location=None,
                 name_location=None, **kwargs):
        self.links = links or set()
        self.name = name
        self.values = values
        self.value_location = value_location
        self.name_location = name_location
        super().__init__(*args, colour=colour or self.default_colour, **kwargs)

    def draw(self):
        super().draw()
        c = self.canvas

        h = self.unit_length
        for direction in self.links:
            tip_of_arrow = (direction.x * (1 - self.arrow_length) * h, direction.y * (1 - self.arrow_length) * h)
            left_side = ((direction.x - math.sin(direction.angle) * self.arrow_width) * h,
                         (direction.y + math.cos(direction.angle) * self.arrow_width) * h)
            right_side = ((direction.x + math.sin(direction.angle) * self.arrow_width) * h,
                          (direction.y - math.cos(direction.angle) * self.arrow_width) * h)

            Draw.polygon(self.canvas, [left_side, tip_of_arrow, right_side], FillStyle(Colour.black))

        if self.name:
            if self.name_location:
                x, y = self.name_location
            elif self.values:
                x, y = 0, -.4
            else:
                x, y = 0, 0
            Draw.text(c, (x*h, y*h), self.name, TextStyle(Font.city_names, Colour.black, 'center', 'center'))

        if self.values:
            if self.value_location:
                x_c, y_c = self.value_location
            elif self.name and self.revenuelocations:
                x_c, y_c = 0, 0.4
            elif self.name:
                x_c, y_c = 0, 0.2
            else:
                x_c, y_c = 0, 0
            for i, v in enumerate(self.values):
                box_size = 8 * mm
                x = (i - len(self.values) / 2) * box_size + x_c * self.unit_length
                y = y_c * self.unit_length - box_size / 2
                Draw.rectangle(c, (x, y), box_size, box_size, FillStyle(Colour.white), LineStyle(Colour.black, 1))
                Draw.text(c, (x + box_size / 2, y_c * self.unit_length), v,
                          TextStyle(Font.normal, Colour.black, 'center', 'center'))

        return self.canvas


class LocationOnHexag:
    """Location on hexag, in units of hexag.unit_lenght (= distance center to flat edge)"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def angle(self):
        return math.atan2(self.y, self.x)

    def xy(self, unit_length=1):
        return self.x * unit_length, self.y * unit_length


class HexagEdge(LocationOnHexag):
    def __init__(self, angle):
        self._angle = angle
        super().__init__(x=math.cos(angle), y=math.sin(angle))

    @property
    def angle(self):
        return self._angle

    @property
    def left_vertex(self):
        return Vertex(angle=self.angle - pi/6)

    @property
    def right_vertex(self):
        return Vertex(angle=self.angle + pi/6)


class Vertex(LocationOnHexag):
    def __init__(self, angle):
        self._angle = angle
        super().__init__(x=2/sqrt(3)*math.cos(angle), y=2/sqrt(3)*math.sin(angle))

    @property
    def angle(self):
        return self._angle


# E, SE, SW, W, NW, NE = Hexag.tile_sides(HORIZONTAL)
# SE, S, SW, NW, N, NE = Hexag.tile_sides(VERTICAL)

def tile_sides(orientation):
    if orientation == VERTICAL:
        start_angle = pi / 6
    else:
        start_angle = 0
    for i in range(6):
        angle = start_angle + i * pi / 3
        yield HexagEdge(angle=angle)


center_of_hexag = LocationOnHexag(0, 0)


class Connect:
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

    @property
    def revenuelocations(self):
        return [x for x in self.args if isinstance(x, City.RevenueLocation)]


class Cost:
    def __init__(self, cost, x=None, y=None):
        self.cost = cost
        self.x = x
        self.y = y

    def draw(self, canvas, x_default, y_default):
        """Draw the image at the location given by self.x, self.y (or at default location)"""
        x = self.x * 20*mm if self.x is not None else x_default     # TODO: unit_length
        y = self.y * 20 * mm if self.y is not None else y_default

        self.draw_at_xy(canvas, x, y)

    def draw_at_xy(self, canvas, x, y):
        """Draw the image at the given location."""
        pass


class Hill(Cost):
    def draw_at_xy(self, canvas, x, y):
        Draw.triangle(canvas, (x, y), 10*mm, FillStyle(Colour.brown), LineStyle(Colour.black, 1))
        Draw.text(canvas, (x, y+2.5*mm), self.cost, TextStyle(Font.normal, Colour.black, 'bottom', 'center'))


class Water(Cost):
    def draw_at_xy(self, canvas, x, y):
        Draw.triangle(canvas, (x, y), 10.5*mm, FillStyle(Colour.lightblue), LineStyle(Colour.black, 1))
        Draw.text(canvas, (x, y + 2.5 * mm), self.cost, TextStyle(Font.normal, Colour.black, 'bottom', 'center'))


class TrackStyle:
    pass


BlackTrack = TrackStyle()
WhiteTrack = TrackStyle()
DottedTrack = TrackStyle()


class Border:
    def __init__(self, hex_edge, colour):
        self.hex_edge = hex_edge
        self.colour = colour
        self.hexag = None

    def draw(self, canvas):
        x, y = self.hexag.location_on_map()
        u = self.hexag.unit_length

        dx1, dy1 = self.hex_edge.left_vertex.xy(unit_length=u)
        dx2, dy2 = self.hex_edge.right_vertex.xy(unit_length=u)

        Draw.line(canvas, (x+dx1, y+dy1), (x+dx2, y+dy2), LineStyle(self.colour or Colour.black,
                                                                     2*mm, end_cap=Draw.end_cap_round))


class Label:
    def __init__(self, text, location=None):
        self.text = text
        self.location = location


empty = Hexag
