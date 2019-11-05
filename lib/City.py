from Output import mm
import Output
import Colour
from math import pi
import math


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
        c.set_source_rgb(*Colour.black)
        Output.draw_text(str(self.value), 'FreeSans', 7, c, x, y, 'center', 'center')
        c.stroke()
        c.set_line_width(1)
        c.arc(x, y, 3 * mm, 0, 2 * pi)
        c.stroke()

    def draw_name(self, hexag):
        if self.name:
            c = hexag.context
            c.set_source_rgb(*Colour.black)
            if self.name_location is None:
                if self.x > 0.4:
                    self.name_location = (-.2, 0, 'center', 'right')
                elif self.x < -0.4:
                    self.name_location = (.2, 0, 'center', 'left')
                else:
                    self.name_location = (0, -.2, 'bottom', 'center')
            if len(self.name_location) < 4:
                self.name_location += ('center', 'center')
            Output.draw_text(self.name, 'FreeSans Italic', 8, c,
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

    def draw(self, hexag):
        context = hexag.context
        City._draw_circle(context, self.x*hexag.unit_length, self.y*hexag.unit_length)

        for c in self.companies:
            c.paint_logo(context, self.x*hexag.unit_length, self.y*hexag.unit_length)

    @classmethod
    def _draw_circle(cls, context, x, y):
        import Company

        city_radius = Company.logo_radius * 1.1

        context.set_source_rgb(*Colour.white)
        context.arc(x, y, city_radius, 0, 2 * pi)
        context.fill_preserve()
        context.set_source_rgb(*Colour.black)
        context.set_line_width(cls.border_width)
        context.stroke()


class DoubleCity(City):
    default_value_location = (0.4, -0.7)

    def draw(self, hexag):
        import Company

        context = hexag.context

        city_radius = Company.logo_radius * 1.1

        context.rectangle(self.x*hexag.unit_length - city_radius, self.y*hexag.unit_length - city_radius,
                          2*city_radius, 2*city_radius)
        context.set_source_rgb(*Colour.white)
        context.set_line_width(self.border_width)
        context.fill_preserve()
        context.set_source_rgb(*Colour.black)
        context.stroke()

        for i in (0, 1):
            x = self.x*hexag.unit_length + (2*i - 1)*city_radius
            y = self.y*hexag.unit_length
            City._draw_circle(context, x, y)

            if len(self.companies) > i:
                company = self.companies[i]
                company.paint_logo(context, x, y)


class Town(RevenueLocation):
    length_bar = .4    # as fraction of hex unit length
    radius = .2
    bar_width = 3 * mm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle = None

    def draw(self, hexag):
        c = hexag.context
        if self.angle is None:
            c.set_source_rgb(*Colour.white)
            c.arc(self.x, self.y, self.radius*hexag.unit_length + 0.5*mm, 0, 2*pi)
            c.fill()
            c.set_source_rgb(*Colour.black)
            c.arc(self.x, self.y, self.radius*hexag.unit_length, 0, 2*pi)
            c.fill()
        else:
            dx_bar = self.length_bar * math.cos(self.angle)
            dy_bar = self.length_bar * math.sin(self.angle)
            c.move_to((self.x - dx_bar/2)*hexag.unit_length, (self.y - dy_bar/2)*hexag.unit_length)
            c.line_to((self.x + dx_bar/2)*hexag.unit_length, (self.y + dy_bar/2)*hexag.unit_length)
            c.set_line_width(self.bar_width)
            c.set_source_rgb(*Colour.black)
            c.stroke()

            if self.value_location is None:
                self.value_location = (dx_bar*1.2, dy_bar*1.2)
