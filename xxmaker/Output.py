import collections
from Definitions import *
from graphics.cairo import Draw
import Colour
from graphics.cairo.Draw import LineStyle, FillStyle, TextStyle
import Font


def tile_register_marks(page, margin, tile):
    # Horizontal lines
    y = margin
    while y <= page.height - margin:
        Draw.line(page, (0, y), (page.width, y), LineStyle(Colour.black, 1))
        y += tile.height

    # Diagonal lines
    x_top = margin + tile.width/4 + margin/3**.5
    x_bottom = x_top - page.height/3**.5
    while x_bottom <= page.width - margin:
        Draw.line(page, (x_top, 0), (x_bottom, page.height), LineStyle(Colour.black, 1))
        x_top += tile.width
        x_bottom += tile.width

    x_top = margin + tile.width*(page.height//tile.width + 3/4) - margin/3**.5
    x_bottom = x_top + page.height/3**.5
    while x_bottom >= margin:
        Draw.line(page, (x_top, 0), (x_bottom, page.height), LineStyle(Colour.black, 1))
        x_top -= tile.width
        x_bottom -= tile.width

    Draw.rectangle(page, (margin-2*mm, margin-2*mm), page.width - 2*margin + 4*mm, page.height - 2*margin + 4*mm,
                   FillStyle(Colour.white))


class Output:
    paper_width = A4_WIDTH
    paper_height = A4_HEIGHT

    def __init__(self, game, margin=10*mm, output_file='out'):
        self.game = game
        self.margin = margin
        self.output_file = output_file
        self.document = None

    def generate(self):
        self.document = Draw.Document(self.output_file + '.ps', self.paper_width, self.paper_height, 10*mm)

        papers = []

        for map_ in self.game.maps:
            papers.append(map_.paper())

        if self.game.stockmarket:
            papers.append(self.game.stockmarket.paper())

        for company in self.game.companies.values():
            papers += list(company.share_papers())
            papers.append(company.charter())

        for number, train in self.game.trains:
            papers += [train.paper()] * number

        for private in self.game.privates:
            papers.append(private.paper())

        for paper in self.game.papers:
            papers.append(paper)

        papers_by_dimension = collections.defaultdict(list)
        for paper in papers:
            paper_parts = list(paper.split_into_parts(self.document.width-2*self.margin,
                                                      self.document.height-2*self.margin))
            papers_by_dimension[(paper_parts[0].width, paper_parts[0].height)] += paper_parts

        for paper_list in papers_by_dimension.values():
            self.document.add_papers(paper_list)

        page = self.document.new_page()
        current_x_left = self.margin
        current_y_top = self.margin
        current_line = 0
        tile_register_marks(page, self.margin, self.game.tiles[0])
        for tile in self.game.tiles:
            if current_x_left + tile.width >= self.document.width - self.margin:
                current_y_top += tile.height
                current_line += 1
                current_x_left = self.margin + tile.width * (current_line % 2) / 2
                if current_y_top + tile.height >= self.document.height - self.margin:
                    page = self.document.new_page()
                    tile_register_marks(page, self.margin, tile)
                    current_x_left = self.margin
                    current_y_top = self.margin
                    current_line = 0

            page.draw(tile.draw(), (current_x_left + tile.width/2, current_y_top+tile.height/2))
            current_x_left += tile.width

        page = self.document.new_page()

        # Tokens
        size = 2*logo_radius + 4*mm
        number_per_row = self.document.width // size - 2

        for i, token in enumerate(self.game.tokens):
            x = self.margin + (i % number_per_row) * size
            y = self.margin + (i // number_per_row) * size
            page.draw(token.draw_sticker(), (x, y))

        self.create_credits_page()
        self.document.finish()

    def create_credits_page(self):
        page = self.document.new_page()
        x = self.margin
        y = self.margin
        for credits_txt in [self.game.credits] + list(self.document.credits_info.values()):
            for line_of_text in credits_txt.split('\n'):
                Draw.text(page, (x, y), line_of_text, TextStyle(Font.small, Colour.black))
                y += 3*mm
