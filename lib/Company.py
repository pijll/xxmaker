import cairo
import Paper
from Output import mm
import Output
import Colour


logo_radius = 5.5*mm


class Company:
    token_costs_default = ['', 40, 100]
    token_interspace = 4*mm

    def __init__(self, name, abbreviation, colour, n_stations, num_shares=10, logo=None, token_costs=None):
        self.name = name
        self.abbreviation = abbreviation
        self.colour = colour
        self.n_stations = n_stations
        self.num_shares = num_shares
        self.token_costs = token_costs
        if logo:
            self.logo = self._make_logo_from_image('../../../graphics/companies/' + logo, radius=logo_radius)
        else:
            self.logo = self._make_logo_from_abbrev(self.abbreviation, radius=logo_radius)
        self.game = None

    def charter(self):
        width = 130 * mm
        height = 90 * mm
        margin = 5 * mm
        height_namebar = 15*mm
        width_train_section = 0.4 * width
        height_tokenbar = height_namebar

        charter = Paper.Paper(width, height)

        c = charter.context

        c.rectangle(margin, margin, width - 2*margin, height_namebar)
        c.set_source_rgb(*self.colour.rgb)
        c.fill_preserve()
        c.set_source_rgb(*Colour.black.rgb)
        c.set_line_width(1*mm)
        c.stroke()

        if self.colour.brightness() > 0.5:
            c.set_source_rgb(*Colour.black.rgb)
        else:
            c.set_source_rgb(*Colour.white.rgb)
        Output.draw_text(self.name, 'Tex Gyre Schola bold', height_namebar/3, c, width/2 + height_tokenbar/2, margin + height_namebar/2,
                         'center', 'center')
        self.paint_logo(c, margin + height_namebar/2, margin + height_namebar/2)

        c.set_source_rgb(*Colour.black.rgb)
        c.rectangle(margin, margin, width - 2*margin, height - 2*margin)
        c.stroke()

        token_costs = self.token_costs or self.token_costs_default
        for i in range(self.n_stations):
            c.set_line_width(0.6*mm)
            x = margin + self.token_interspace*(i+1) + logo_radius*(2*i + 1)
            y = margin + height_namebar + self.token_interspace + logo_radius
            c.arc(x, y, logo_radius, 0, 6.29)
            c.stroke()

            try:
                token_cost = token_costs[i]
            except IndexError:
                token_cost = token_costs[-1]
            if token_cost:
                Output.draw_text(f'{self.game.currency}{token_cost}', 'FreeSans', 8, c, x, y+logo_radius, 'top', 'center')
                c.stroke()

        return charter

    def share_papers(self):
        yield self._share_paper(percentage=int(100/self.num_shares*2), director=True)

        for i in range(self.num_shares-2):
            yield self._share_paper(percentage=int(100/self.num_shares))

    def _share_paper(self, percentage, director=False):
        share = Paper.Paper()
        c = share.context

        c.set_source_rgba(*self.colour.rgb, 0.1)
        c.paint()

        c.set_source_rgb(*self.colour.rgb)
        c.rectangle(3*mm, 0, 13*mm, share.height)
        c.fill()

        c.set_source_rgb(*Colour.black.rgb)

#        c.move_to(10*mm, 10*mm)
#        c.show_text(self.name)

        Output.draw_centered_lines(self.name, 'Tex Gyre Schola bold', 8, c,
                                   x_c=(share.width + 16*mm)/2, y=14 * mm,
                                   width=share.width - 16*mm - 6*mm)

        number_of_shares = 'Two shares' if director else 'One share'
        Output.draw_text(number_of_shares, "Tex Gyre Schola", 7, c,
                         x=19*mm, y=share.height-3*mm, valign='bottom', halign='left')
        Output.draw_text(f"{percentage}%", "Tex Gyre Schola", 7, c,
                         x=share.width-3*mm, y=share.height-3*mm, valign='bottom', halign='right')

        self.paint_logo(c, 9.5*mm, 11.5*mm)
        if director:
            self.paint_logo(c, 9.5*mm, 27.5*mm)

        return share

    def _make_logo_from_image(self, logo_file, radius):
        surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, 2*radius, 2*radius))
        context = cairo.Context(surface)
        context.set_source_rgb(*Colour.white.rgb)
        context.arc(radius, radius, radius, 0, 6.29)
        context.fill()
        Output.load_image(logo_file, context, radius, radius, radius * 1.9, radius * 1.9, circle_clip=True)
        return surface

    def _make_logo_from_abbrev(self, abbreviation, radius):
        surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, 2 * radius, 2 * radius))
        context = cairo.Context(surface)
        context.set_source_rgb(*Colour.white.rgb)
        context.arc(radius, radius, radius, 0, 6.29)
        context.fill()

        context.set_source_rgb(*Colour.black.rgb)
        # context.set_font_size(1)
        # text_width = context.text_extents(abbreviation)[2]
        # scaling = radius*2 / text_width
        # context.set_font_size(scaling)
        #
        # x_bearing, y_bearing, width, height, *_ = context.text_extents(abbreviation)
        #
        # context.move_to(radius - width/2 - x_bearing, radius - height/2 - y_bearing)
        # context.show_text(abbreviation)
        Output.draw_text(abbreviation, 'Woodcut', 8, context, radius, radius+1*mm, 'center', 'center')

        return surface

    def paint_logo(self, context, xc, yc):
        context.set_source_surface(self.logo, xc - logo_radius, yc-logo_radius)
        context.paint()

#
# class ShareCertificate:
#     def __init__(self, company, percentage, director=False):
#         self.company = company,
#         self.percentage = percentage
#         self.director = director
#
