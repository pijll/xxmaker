import Colour
from graphics.cairo import Draw
from .Paper import Paper, mm


class IPO(Paper):
    outside_margin = 5*mm
    inner_margin = 5*mm

    def __init__(self, game, number_of_columns=None):
        company_shares = [company.share_paper(percentage=None) for company in game.companies.values()]

        if number_of_columns is None:
            if len(company_shares) >= 7:
                number_of_columns = 3
            else:
                number_of_columns = 2

        share_height = max(p.height for p in company_shares)
        number_of_rows = (len(company_shares) - 1) // number_of_columns + 1
        height = 2*self.outside_margin + number_of_rows * share_height + (number_of_rows-1) * self.inner_margin

        share_width = max(p.width for p in company_shares)
        width = 2*self.outside_margin + + number_of_columns * share_width + (number_of_columns-1) * self.inner_margin

        super().__init__(width=width, height=height)
        c = self.canvas

        for i, company_paper in enumerate(company_shares):
            row = i // number_of_columns
            column = i % number_of_columns

            x = self.outside_margin + (share_width + self.inner_margin) * column
            y = self.outside_margin + (share_height + self.inner_margin) * row
            c.draw(company_paper.canvas, (x, y), black_and_white=True, alpha=0.5)
            Draw.rectangle(c, (x, y), company_paper.width, company_paper.height, Draw.LineStyle(Colour.black, 2))
