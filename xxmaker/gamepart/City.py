from Definitions import mm
import Colour
import math
import Font
from . import Company
from graphics.cairo import Draw
from graphics.cairo.Draw import LineStyle, FillStyle, TextStyle


class RevenueLocation:
    default_value_location = (0.7, 0)
    name_distance = 0.4

    def __init__(self, id_=None, name=None, value=None, x=None, y=None, location=0.5, name_location=None,
                 value_location=None):
        self.id = id_ or name
        self.name = name
        self.x = x
        self.y = y
        self.location = location
        self.name_location = name_location
        if isinstance(value, Value):
            self.value = value
        else:
            self.value = Value(value, value_location)
        self.hexag = None

    def draw(self, canvas, hex_location):
        raise NotImplemented

    def draw_value(self, canvas, hex_location):
        xc, yc = hex_location
        if self.value.value is None:
            return
        if self.value.location is None:
            self.value.location = self.default_value_location
        x = (self.x + self.value.location[0]) * self.hexag.unit_length + xc
        y = (self.y + self.value.location[1]) * self.hexag.unit_length + yc

        Draw.text(canvas, (x, y), self.value.value, TextStyle(Font.city_value, Colour.black, 'exactcenter', 'exactcenter'))
        Draw.circle(canvas, (x, y), 3 * mm, LineStyle(Colour.black, 1))

    def draw_name(self, canvas, hex_location):
        xc, yc = hex_location
        if self.name:
            if self.name_location is None:
                if self.x > 0.4:
                    self.name_location = (-.4, 0, 'center', 'right')
                elif self.x < -0.4:
                    self.name_location = (.4, 0, 'center', 'left')
                elif self.hexag.cost:
                    self.name_location = (0, self.name_distance, 'top', 'center')
                else:
                    self.name_location = (0, -self.name_distance, 'bottom', 'center')
            if len(self.name_location) < 4:
                self.name_location += ('center', 'center')
            Draw.text(canvas, ((self.x+self.name_location[0]) * self.hexag.unit_length + xc,
                                     (self.y+self.name_location[1]) * self.hexag.unit_length + yc),
                      self.name, TextStyle(Font.city_names, Colour.black,
                                           valign=self.name_location[2], halign=self.name_location[3]))


class City(RevenueLocation):
    border_width = 0.5*mm

    def __init__(self, id_=None, value=None, x=None, y=None, location=0.5, name=None,
                 name_location=None, value_location=None, companies=None):
        super().__init__(name=name, value=value, x=x, y=y, location=location, name_location=name_location,
                         value_location=value_location, id_=id_)
        self.companies = companies or []

    city_radius = Company.logo_radius * 1.1

    def draw(self, canvas, hex_location):
        xc, yc = hex_location
        City._draw_circle(canvas, (self.x * self.hexag.unit_length + xc, self.y * self.hexag.unit_length + yc))

        for c in self.companies:
            c.token.draw_on_color(canvas, self.x * self.hexag.unit_length + xc, self.y * self.hexag.unit_length + yc)

    @classmethod
    def _draw_circle(cls, canvas, location):
        radius = cls.city_radius

        Draw.circle(canvas, location, radius, FillStyle(Colour.white), LineStyle(Colour.black, cls.border_width))


class DoubleCity(City):
    default_value_location = (0.4, -0.7)

    def draw(self, canvas, hex_location):
        xc, yc = hex_location
        city_radius = self.city_radius

        Draw.rectangle(canvas, (self.x*self.hexag.unit_length - city_radius + xc, self.y*self.hexag.unit_length - city_radius+yc),
                       2*city_radius, 2*city_radius, FillStyle(Colour.white), LineStyle(Colour.black, self.border_width))

        for i in (0, 1):
            x = self.x*self.hexag.unit_length + (2*i - 1)*city_radius +xc
            y = self.y*self.hexag.unit_length +yc
            City._draw_circle(canvas, (x, y))

            if len(self.companies) > i:
                company = self.companies[i]
                company.paint_logo(canvas, x, y)


class TripleCity(City):
    default_value_location = (0.4, -0.7)

    def draw(self, canvas, hex_location):
        xc, yc = hex_location
        city_radius = self.city_radius

        polygon = ((-1, -3**.5/3-1), (1, -3**.5/3-1), (1+3**.5/2, -3**.5/3+.5),
                   (3**.5/2, 2*3**.5/3+.5), (-3**.5/2, 2*3**.5/3+.5), (-1-3**.5/2, -3**.5/3+.5))
        points = [(x*city_radius + xc, y*city_radius + yc) for (x, y) in polygon]
        Draw.polygon(canvas, points, FillStyle(Colour.white), LineStyle(Colour.black, self.border_width))

        city_locations = [(-1, -(3**.5)/3), (+1, -(3**.5)/3), (0, 2*(3**.5)/3)]

        for i, (x_1, y_1) in enumerate(city_locations):
            x = self.x*self.hexag.unit_length + x_1 * city_radius + xc
            y = self.y*self.hexag.unit_length + y_1 * city_radius + yc
            City._draw_circle(canvas, (x, y))

            if len(self.companies) > i:
                company = self.companies[i]
                company.paint_logo(canvas, x, y)


class QuadCity(City):
    default_value_location = (0.45, -0.8)

    def draw(self, canvas, hex_location):
        xc, yc = hex_location
        city_radius = self.city_radius

        polygon = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
        points = [(x*city_radius + xc, y*city_radius + yc) for (x, y) in polygon]
        Draw.polygon(canvas, points, FillStyle(Colour.white), LineStyle(Colour.black, self.border_width))

        city_locations = [(-1, -1), (+1, -1), (-1, +1), (+1, +1)]

        for i, (x_1, y_1) in enumerate(city_locations):
            x = self.x*self.hexag.unit_length + x_1 * city_radius + xc
            y = self.y*self.hexag.unit_length + y_1 * city_radius + yc
            City._draw_circle(canvas, (x, y))

            if len(self.companies) > i:
                company = self.companies[i]
                company.paint_logo(canvas, x, y)


class Town(RevenueLocation):
    length_bar = .4    # as fraction of hex unit length
    radius = .12
    bar_width = 3 * mm
    name_distance = 0.25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle = None

    def draw(self, canvas, hex_location):
        xc, yc = hex_location
        if self.angle is None:
            Draw.circle(canvas, (self.x * self.hexag.unit_length + xc, self.y * self.hexag.unit_length + yc),
                        self.radius * self.hexag.unit_length + 0.5 * mm, FillStyle(Colour.black), LineStyle(Colour.white, 0.5*mm))
        else:
            dx_bar = self.length_bar * math.cos(self.angle)
            dy_bar = self.length_bar * math.sin(self.angle)
            Draw.line(canvas, ((self.x - dx_bar / 2) * self.hexag.unit_length + xc, (self.y - dy_bar / 2) * self.hexag.unit_length + yc),
                      ((self.x + dx_bar/2)*self.hexag.unit_length + xc, (self.y + dy_bar/2)*self.hexag.unit_length + yc),
                      LineStyle(Colour.black, self.bar_width))

            if self.value.location is None:
                self.value.location = (dx_bar*1.2, dy_bar*1.2)


class Port(City):
    def draw(self, hexag, hex_location):
        canvas = hexag.canvas_foreground
        Draw.load_image(canvas, 'misc/anchor.svg', hex_location, 12*mm, 12*mm)


class Value:
    def __init__(self, value, location=None):
        self.value = value
        self.location = location
