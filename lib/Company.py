import cairo
import Paper
from Definitions import mm
import OutputFunctions
import Colour
import Font
import Draw
from Draw import FillStyle, LineStyle, TextStyle


logo_radius = 5.5*mm


class Company:
    token_costs_default = ['', 40, 100]
    token_interspace = 4*mm

    def __init__(self, name, abbreviation, colour, n_stations=0, num_shares=10,
                 logo=None, logo_zoom=1, token_costs=None,
                 par_price=None, marker=None):
        self.name = name
        self.abbreviation = abbreviation
        self.colour = colour
        self.n_stations = n_stations
        self.num_shares = num_shares
        self.token_costs = token_costs
        if logo:
            self.logo = self._make_logo_from_image('companies/' + logo, radius=logo_radius, zoom=logo_zoom)
        else:
            self.logo = self._make_logo_from_abbrev(self.abbreviation, radius=logo_radius)
        self.game = None
        self.par_price = par_price
        self.marker = marker

    def charter(self):
        width = 130 * mm
        height = 90 * mm
        margin = 5 * mm
        height_namebar = 15*mm
        width_train_section = 0.4 * width
        height_tokenbar = height_namebar

        charter = Paper.Paper(width, height, marker=self.marker)

        c = charter.canvas

        Draw.rectangle(c, (margin, margin), width - 2*margin, height_namebar, FillStyle(self.colour), LineStyle(Colour.black, 1*mm))
        Draw.text(c, (width / 2 + height_tokenbar / 2, margin + height_namebar / 2), self.name,
                  TextStyle(Font.charter_name, self.colour.contrast_colour, 'center', 'center'))

        self.paint_logo(c, margin + height_namebar/2, margin + height_namebar/2)

        Draw.rectangle(c, (margin, margin), width - 2*margin, height - 2*margin, LineStyle(Colour.black, 1*mm))

        if callable(self.token_costs):
            self.token_costs(company=self, canvas=c,
                             location=(margin + self.token_interspace*(self.n_stations+1)/2 + logo_radius*self.n_stations,
                                       margin + height_namebar + self.token_interspace + 2 * logo_radius))
            token_costs = None
        elif self.token_costs:
            token_costs = self.token_costs
        else:
            token_costs = self.token_costs_default

        for i in range(self.n_stations):
            x = margin + self.token_interspace*(i+1) + logo_radius*(2*i + 1)
            y = margin + height_namebar + self.token_interspace + logo_radius
            Draw.circle(c, (x,y), logo_radius, LineStyle(Colour.black, 0.6*mm))

            if token_costs:
                try:
                    token_cost = token_costs[i]
                except IndexError:
                    token_cost = token_costs[-1]
                if token_cost:
                    Draw.text(c, (x, y+logo_radius), f'{self.game.currency}{token_cost}',
                              TextStyle(Font.normal, Colour.black, 'top', 'center'))

        return charter

    def share_papers(self):
        yield self._share_paper(percentage=int(100/self.num_shares*2), director=True)

        for i in range(self.num_shares-2):
            yield self._share_paper(percentage=int(100/self.num_shares))

    def _share_paper(self, percentage, director=False):
        share = Paper.Certificate(colour=self.colour, price=self.par_price, name=self.name, marker=self.marker)
        c = share.canvas

        number_of_shares = 'Two shares' if director else 'One share'
        Draw.text(c, (19*mm, share.height-3*mm), number_of_shares,
                  TextStyle(Font.normal, Colour.black, 'bottom', 'left'))
        Draw.text(c, (share.width-3*mm, share.height-3*mm), f'{percentage}%',
                  TextStyle(Font.normal, Colour.black, 'bottom', 'right'))

        self.paint_logo(c, 9.5*mm, 11.5*mm)
        if director:
            self.paint_logo(c, 9.5*mm, 27.5*mm)

        return share

    def _make_logo_from_image(self, logo_file, radius, zoom=1):
        return OutputFunctions.put_image_on_token(logo_file, radius, zoom)

    def _make_logo_from_abbrev(self, abbreviation, radius):
        canvas = Draw.Canvas((0,0), 2*radius, 2*radius)
        Draw.circle(canvas, (radius, radius), radius, FillStyle(Colour.white))
        Draw.circle(canvas, (radius, radius), radius*0.9, LineStyle(self.colour, 0.5*mm))

        font = Font.certificate_name.made_to_fit(abbreviation, canvas, radius*1.6)

        Draw.text(canvas, (radius, radius), abbreviation,
                  TextStyle(font, Colour.black, 'exactcenter', 'exactcenter'))

        return canvas

    def paint_logo(self, canvas, xc, yc):
        canvas.draw(self.logo, (xc - logo_radius, yc-logo_radius))
