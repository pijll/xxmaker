from Definitions import *
import math
from math import sqrt, pi

import Colour
from . import City
import Font
from graphics.cairo import Draw
from graphics.cairo.Draw import LineStyle, FillStyle, TextStyle
from . import Connect

hexag_size = 40 * mm  # edge to edge


class Hexag:
    def __init__(self, *args, colour=None, size=None, outline=True, label=None, label_location=None,
                 orientation=None, cost=None, no_border=None, row=None, column=None, icon=None, alpha=None):
        self.size = size or hexag_size
        self.canvas = None
        self.canvas_foreground = None
        self.colour = colour or Colour.background
        self.outline = outline
        self.label = Label(label, label_location) if label is not None else None
        self.cost = cost
        if cost:
            cost.hexag = self
        self.orientation = orientation
        self.no_border = no_border or []
        self.row = row
        self.column = column
        self.icon = icon
        self.alpha = alpha

        self.revenuelocations = []
        self.connections = []
        self.borders = []
        for arg in args:
            if isinstance(arg, City.RevenueLocation):
                self.revenuelocations.append(arg)
                arg.hexag = self
            elif isinstance(arg, Connect.Connect):
                self.connections.append(arg)
                arg.hexag = self
                self.revenuelocations += arg.revenuelocations
                for loc in arg.revenuelocations:
                    loc.hexag = self
            elif isinstance(arg, Cost):
                self.cost = arg
                arg.hexag = self
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
        self.draw_on_canvas(self.canvas, (0, 0))

        return self.canvas

    def draw_on_canvas(self, canvas, location):
        self.draw_background(canvas, location)
        self.draw_foreground(canvas, location)

    def draw_background(self, canvas, location):
        """Draw the background of the tile.

        Because this background sometimes needs to be transparent, it is painted directly on the canvas,
        instead of on its own canvas.

        Paramters:
        - canvas
        - location, the centerpoint coordinate of the hex (in coordinates of the canvas)
        """
        xc, yc = location
        if self.colour != Colour.transparent:
            vertices = self.vertices()
            points = [v.xy(unit_length=self.unit_length) for v in vertices]
            Draw.polygon(canvas, [(x+xc, y+yc) for x, y in points], FillStyle(colour=self.colour, alpha=self.alpha))

    def draw_foreground(self, canvas, location):
        if False:
            foreground = self.foreground_canvas()
            canvas.draw(foreground, location)
        else:
            self.draw_foreground_on_canvas(canvas, location)

    def draw_foreground_on_canvas(self, canvas, location):
        h = self.unit_length

        self.set_city_coordinates()

        named_location = {city.id: city for city in self.revenuelocations}
        for conn in self.connections:
            if isinstance(conn.side1, str):
                conn.side1 = named_location[conn.side1]
            if isinstance(conn.side2, str):
                conn.side2 = named_location[conn.side2]

            if isinstance(conn.side2, HexagEdge) and not isinstance(conn.side1, HexagEdge):
                conn.side1, conn.side2 = conn.side2, conn.side1

        self.draw_connections(canvas, hex_location=location)

        for i, city in enumerate(self.revenuelocations):
            city.draw(canvas, location)
            city.draw_name(canvas, location)
            city.draw_value(canvas, location)

        if self.cost:
            self.cost.draw(canvas, location)

        if self.label:
            self.draw_label(canvas, location)

        # if self.icon:
        #     c.draw(self.icon, (-0.5, 0.4))
        #
        if self.outline:
            self.draw_outline(canvas, location)

    def draw_outline(self, canvas, hex_location):
        xc, yc = hex_location
        hex_edges = list(tile_sides(self.orientation))
        for hex_edge in hex_edges:
            if hex_edge not in self.no_border:
                x_start, y_start = hex_edge.left_vertex.xy(unit_length=self.unit_length)
                x_end, y_end = hex_edge.right_vertex.xy(unit_length=self.unit_length)
                Draw.line(canvas, (x_start + xc, y_start + yc), (x_end + xc, y_end + yc),
                          LineStyle(Colour.black, 1))

    def set_city_coordinates(self):
        for i, city in enumerate(self.revenuelocations):
            if city.x is None or city.y is None:
                if len(self.revenuelocations) == 1:
                    city.x, city.y = 0, 0
                elif len(self.revenuelocations) == 2:
                    if self.orientation == HORIZONTAL:
                        city.x, city.y = 0.6, -0.3
                    else:
                        city.x, city.y = 0.45, -0.3
                    if i == 1:
                        city.x, city.y = -city.x, -city.y

    def foreground_canvas(self):
        if self.canvas_foreground:
            return self.canvas_foreground

        self.canvas_foreground = Draw.Canvas((-self.width, -self.height), 2 * self.width, 2 * self.height)
        c = self.canvas_foreground

        h = self.unit_length

        cities = dict()
        for ct in self.revenuelocations:
            cities[ct.id] = ct

        self.set_city_coordinates()

        for conn in self.connections:
            if isinstance(conn.side1, str):
                conn.side1 = cities[conn.side1]
            if isinstance(conn.side2, str):
                conn.side2 = cities[conn.side2]

            if isinstance(conn.side2, HexagEdge) and not isinstance(conn.side1, HexagEdge):
                conn.side1, conn.side2 = conn.side2, conn.side1

        self.draw_connections(self.canvas_foreground)

        for i, city in enumerate(self.revenuelocations):
            city.draw(self.canvas_foreground, (0, 0))
            city.draw_name(self.canvas_foreground, (0, 0))
            city.draw_value(self.canvas_foreground, (0, 0))

        if self.cost:
            self.cost.draw(c)

        if self.label:
            if self.label.location:
                x, y = self.label.location
            else:
                # x, y = (0.7, 0.05)
                x, y = (-0.5, -0.75)
            Draw.text(c, (x*h, y*h), self.label.text, TextStyle(Font.label, Colour.black, 'center', 'left'))

        if self.icon:
            c.draw(self.icon, (-0.5, 0.4))

        if self.outline:
            hex_edges = list(tile_sides(self.orientation))
            for hex_edge in hex_edges:
                if hex_edge not in self.no_border:
                    xy_start = hex_edge.left_vertex.xy(unit_length=self.unit_length)
                    xy_end = hex_edge.right_vertex.xy(unit_length=self.unit_length)
                    Draw.line(c, xy_start, xy_end, LineStyle(Colour.black, 1))

        return self.canvas_foreground

    def cost_location(self):
        """Returns the default location of a cost symbol on this hexag.

        Units are in mm from the centre of the hex.
        """
        if self.revenuelocations:
            y = - self.revenuelocations[0].name_distance * self.unit_length - 3 * mm
        else:
            y = 0
        return 0, y

    def draw_connections(self, canvas, hex_location=(0, 0)):
        for conn in self.connections:
            if not conn.over:
                conn.draw_background(canvas, hex_location)
        for conn in self.connections:
            if conn.under:
                conn.draw_foreground(canvas, hex_location)
        for conn in self.connections:
            if conn.over:
                conn.draw_background(canvas, hex_location)
        for conn in self.connections:
            if not conn.under:
                conn.draw_foreground(canvas, hex_location)

    def label_location(self):
        return 0.7, 0.05

    def draw_label(self, canvas, hex_location=(0, 0)):
        label_x, label_y = self.label.location or self.label_location()
        xc, yc = hex_location
        h = self.unit_length
        Draw.text(canvas, (label_x*h + xc, label_y*h + yc), self.label.text, TextStyle(Font.label, Colour.black, 'center', 'left'))


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

    def draw_foreground(self, canvas, location):
        super().draw_foreground(canvas, location)
        xc, yc = location
        h = self.unit_length
        for direction in self.links:
            tip_of_arrow = (direction.x * (1 - self.arrow_length) * h + xc, direction.y * (1 - self.arrow_length) * h + yc)
            left_side = ((direction.x - math.sin(direction.angle) * self.arrow_width) * h + xc,
                         (direction.y + math.cos(direction.angle) * self.arrow_width) * h + yc)
            right_side = ((direction.x + math.sin(direction.angle) * self.arrow_width) * h + xc,
                          (direction.y - math.cos(direction.angle) * self.arrow_width) * h + yc)

            Draw.polygon(canvas, [left_side, tip_of_arrow, right_side], FillStyle(Colour.black))

        if self.name:
            if self.name_location:
                x, y = self.name_location
            elif self.values:
                x, y = 0, -.4
            else:
                x, y = 0, 0
            Draw.text(canvas, (x * h + xc, y * h + yc), self.name, TextStyle(Font.city_names, Colour.black, 'center', 'center'))

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
                Draw.rectangle(canvas, (x + xc, y + yc), box_size, box_size, FillStyle(Colour.white), LineStyle(Colour.black, 1))
                Draw.text(canvas, (x + box_size / 2 + xc, y_c * self.unit_length + yc), v,
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

    def __hash__(self):
        return int(self.angle * 1e4)

    def __eq__(self, other):
        return abs(self.angle - other.angle) < 1e-5

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


class Cost:
    def __init__(self, cost, x=None, y=None):
        self.cost = cost
        self.x = x
        self.y = y
        self.hexag = None

    def draw(self, canvas, hex_location=(0,0)):
        """Draw the cost symbol.

        The location is determined by the x and y coordinates in the Cost object,
        or by the other objects on the hex."""
        xc, yc = hex_location
        x_default, y_default = self.hexag.cost_location()
        x = self.x * self.hexag.unit_length if self.x is not None else x_default
        y = self.y * self.hexag.unit_length if self.y is not None else y_default

        self.draw_at_xy(canvas, (x + xc, y + yc))

    def draw_at_xy(self, canvas, location):
        """Draw the image at the given location."""
        pass


class Hill(Cost):
    fill_colour = Colour.brown

    def draw_at_xy(self, canvas, location):
        x, y = location
        Draw.triangle(canvas, (x, y), 10*mm, FillStyle(self.fill_colour), LineStyle(Colour.black, 1))
        Draw.text(canvas, (x, y+2.5*mm), self.cost, TextStyle(Font.normal, self.fill_colour.contrast_colour, 'bottom', 'center'))


class Water(Cost):
    def draw_at_xy(self, canvas, location):
        x, y = location
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


empty = Hexag()
