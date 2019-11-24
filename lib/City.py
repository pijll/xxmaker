from Definitions import mm
import OutputFunctions
import Colour
from math import pi
import math
import Company
import Font


class RevenueLocation:
    default_value_location = (0.7, 0)

    def __init__(self, id_=None, name=None, value=None, x=None, y=None, location=0.5, name_location=None,
                 value_location=None):
        self.id = id_ or name
        self.name = name
        self.x = x
        self.y = y
        self.location = location
        self.name_location = name_location
        self.value = value
        self.value_location = value_location

    def draw_value(self, hexag):
        if self.value is None:
            return
        if self.value_location is None:
            self.value_location = self.default_value_location
        x = (self.x + self.value_location[0]) * hexag.unit_length
        y = (self.y + self.value_location[1]) * hexag.unit_length
        c = hexag.context
        Colour.black.use_in_context(c)
        OutputFunctions.draw_text(self.value, Font.city_value, c, x, y, 'exactcenter', 'exactcenter')
        c.stroke()
        c.set_line_width(1)
        c.arc(x, y, 3 * mm, 0, 2 * pi)
        c.stroke()

    def draw_name(self, hexag):
        if self.name:
            c = hexag.context
            Colour.black.use_in_context(c)
            if self.name_location is None:
                if self.x > 0.4:
                    self.name_location = (-.4, 0, 'center', 'right')
                elif self.x < -0.4:
                    self.name_location = (.4, 0, 'center', 'left')
                elif hexag.cost:
                    self.name_location = (0, .4, 'top', 'center')
                else:
                    self.name_location = (0, -.4, 'bottom', 'center')
            if len(self.name_location) < 4:
                self.name_location += ('center', 'center')
            OutputFunctions.draw_text(self.name, Font.city_names, c,
                                          (self.x+self.name_location[0]) * hexag.unit_length,
                                          (self.y + self.name_location[1]) * hexag.unit_length,
                                          valign=self.name_location[2], halign=self.name_location[3])
            c.stroke()


class City(RevenueLocation):
    border_width = 0.5*mm

    def __init__(self, id_=None, value=None, x=None, y=None, location=0.5, name=None,
                 name_location=None, value_location=None, companies=None):
        super().__init__(name=name, value=value, x=x, y=y, location=location, name_location=name_location,
                         value_location=value_location, id_=id_)
        self.companies = companies or []

    city_radius = Company.logo_radius * 1.1

    def draw(self, hexag):
        context = hexag.context
        City._draw_circle(context, self.x*hexag.unit_length, self.y*hexag.unit_length)

        for c in self.companies:
            c.paint_logo(context, self.x*hexag.unit_length, self.y*hexag.unit_length)

    @classmethod
    def _draw_circle(cls, context, x, y):
        radius = cls.city_radius

        Colour.white.use_in_context(context)
        context.arc(x, y, radius, 0, 2 * pi)
        context.fill_preserve()
        Colour.black.use_in_context(context)
        context.set_line_width(cls.border_width)
        context.stroke()


class DoubleCity(City):
    default_value_location = (0.4, -0.7)

    def draw(self, hexag):
        context = hexag.context
        city_radius = self.city_radius

        context.rectangle(self.x*hexag.unit_length - city_radius, self.y*hexag.unit_length - city_radius,
                          2*city_radius, 2*city_radius)
        Colour.white.use_in_context(context)
        context.set_line_width(self.border_width)
        context.fill_preserve()
        Colour.black.use_in_context(context)
        context.stroke()

        for i in (0, 1):
            x = self.x*hexag.unit_length + (2*i - 1)*city_radius
            y = self.y*hexag.unit_length
            City._draw_circle(context, x, y)

            if len(self.companies) > i:
                company = self.companies[i]
                company.paint_logo(context, x, y)


class TripleCity(City):
    default_value_location = (0.4, -0.7)

    def draw(self, hexag):
        context = hexag.context
        city_radius = self.city_radius

        polygon = ((-1, -3**.5/3-1), (1, -3**.5/3-1), (1+3**.5/2, -3**.5/3+.5),
                   (3**.5/2, 2*3**.5/3+.5), (-3**.5/2, 2*3**.5/3+.5), (-1-3**.5/2, -3**.5/3+.5))
        for i, (x, y) in enumerate(polygon):
            if i == 0:
                context.move_to(x*city_radius, y*city_radius)
            else:
                context.line_to(x*city_radius, y*city_radius)
        context.close_path()

        Colour.white.use_in_context(context)
        context.set_line_width(self.border_width)
        context.fill_preserve()
        Colour.black.use_in_context(context)
        context.stroke()

        city_locations = [(-1, -(3**.5)/3), (+1, -(3**.5)/3), (0, 2*(3**.5)/3)]

        for i, (x_1, y_1) in enumerate(city_locations):
            x = self.x*hexag.unit_length + x_1 * city_radius
            y = self.y*hexag.unit_length + y_1 * city_radius
            City._draw_circle(context, x, y)

            if len(self.companies) > i:
                company = self.companies[i]
                company.paint_logo(context, x, y)


class QuadCity(City):
    default_value_location = (0.45, -0.8)

    def draw(self, hexag):
        context = hexag.context
        city_radius = self.city_radius

        context.move_to(-2*city_radius, -1*city_radius)
        context.line_to(-1*city_radius, -2*city_radius)
        context.line_to(1*city_radius, -2*city_radius)
        context.line_to(2*city_radius, -1*city_radius)
        context.line_to(2*city_radius, 1*city_radius)
        context.line_to(1*city_radius, 2*city_radius)
        context.line_to(-1*city_radius, 2*city_radius)
        context.line_to(-2*city_radius, 1*city_radius)
        context.close_path()

        Colour.white.use_in_context(context)
        context.set_line_width(self.border_width)
        context.fill_preserve()
        Colour.black.use_in_context(context)
        context.stroke()

        city_locations = [(-1, -1), (+1, -1), (-1, +1), (+1, +1)]

        for i, (x_1, y_1) in enumerate(city_locations):
            x = self.x*hexag.unit_length + x_1 * city_radius
            y = self.y*hexag.unit_length + y_1 * city_radius
            City._draw_circle(context, x, y)

            if len(self.companies) > i:
                company = self.companies[i]
                company.paint_logo(context, x, y)


class Town(RevenueLocation):
    length_bar = .4    # as fraction of hex unit length
    radius = .1
    bar_width = 3 * mm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle = None

    def draw(self, hexag):
        c = hexag.context
        if self.angle is None:
            Colour.white.use_in_context(c)
            c.arc(self.x*hexag.unit_length, self.y*hexag.unit_length, self.radius*hexag.unit_length + 0.5*mm, 0, 2*pi)
            c.fill()
            Colour.black.use_in_context(c)
            c.arc(self.x*hexag.unit_length, self.y*hexag.unit_length, self.radius*hexag.unit_length, 0, 2*pi)
            c.fill()
        else:
            dx_bar = self.length_bar * math.cos(self.angle)
            dy_bar = self.length_bar * math.sin(self.angle)
            c.move_to((self.x - dx_bar/2)*hexag.unit_length, (self.y - dy_bar/2)*hexag.unit_length)
            c.line_to((self.x + dx_bar/2)*hexag.unit_length, (self.y + dy_bar/2)*hexag.unit_length)
            c.set_line_width(self.bar_width)
            Colour.black.use_in_context(c)
            c.stroke()

            if self.value_location is None:
                self.value_location = (dx_bar*1.2, dy_bar*1.2)


class Port(City):
    pass
