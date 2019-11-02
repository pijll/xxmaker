from Output import mm
import Colour
from math import pi


class City:
    border_width = 0.5*mm

    def __init__(self, id="", value=20, x=0, y=0, companies=None):
        self.id = id
        self.x = x
        self.y = y
        self.companies = companies or []

    def draw(self, map, context, x, y):
        City._draw_circle(context, x, y)

        for company_abbr in self.companies:
            company = map.game.companies[company_abbr]
            company.paint_logo(context, x, y)

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
    def draw(self, map, context, x, y):
        import Company

        city_radius = Company.logo_radius * 1.1

        context.rectangle(x - city_radius, y - city_radius, 2*city_radius, 2*city_radius)
        context.set_source_rgb(*Colour.white)
        context.set_line_width(self.border_width)
        context.fill_preserve()
        context.set_source_rgb(*Colour.black)
        context.stroke()

        for i in (-1, 1):
            City._draw_circle(context, x + i*city_radius, y)

    # for company_abbr in self.companies:
    #     company = map.game.companies[company_abbr]
    #     company.paint_logo(self.context, x, y)


class Town:
    length_bar = 7*mm

    def __init__(self, value=10, location=0.5):
        self.location = location
