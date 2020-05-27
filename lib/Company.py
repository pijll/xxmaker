import cairo
import Paper
from Definitions import mm
import OutputFunctions
import Colour
import Font
import Draw
from Draw import FillStyle, LineStyle, TextStyle
from Token import Token

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
            self.token = Token(image_file='companies/' + logo, zoom=logo_zoom, background_colour=colour)
        else:
            self.token = Token(text=abbreviation)
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
                  TextStyle(Font.charter_name.made_to_fit(self.name, c, width - height_tokenbar - 2*margin - 4*mm),
                            self.colour.contrast_colour, 'center', 'center'))

        self.token.draw_black_on_white(c, margin + height_namebar/2, margin + height_namebar/2)

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
        yield self.share_paper(percentage=int(100 / self.num_shares * 2), director=True)

        for i in range(self.num_shares-2):
            yield self.share_paper(percentage=int(100 / self.num_shares))

    def share_paper(self, percentage, director=False):
        share = Paper.Certificate(colour=self.colour, price=self.par_price, name=self.name, marker=self.marker)
        c = share.canvas

        if percentage is not None:
            number_of_shares = 'Two shares' if director else 'One share'
            Draw.text(c, (19*mm, share.height-3*mm), number_of_shares,
                      TextStyle(Font.normal, Colour.black, 'bottom', 'left'))
            Draw.text(c, (share.width-3*mm, share.height-3*mm), f'{percentage}%',
                      TextStyle(Font.normal, Colour.black, 'bottom', 'right'))

        self.token.draw_black_on_white(c, 9.5*mm, 11.5*mm)
        if director:
            self.token.draw_black_on_white(c, 9.5*mm, 27.5*mm)

        return share
