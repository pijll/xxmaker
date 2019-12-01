import cairo
import Paper
import collections
import math
from Definitions import *
import subprocess
import Draw
import Colour
from Draw import LineStyle, FillStyle, TextStyle


A4_WIDTH_IN_MM = 210
A4_HEIGHT_IN_MM = 297

A4_WIDTH_IN_PT = int(A4_WIDTH_IN_MM / 25.4 * 72)
A4_HEIGHT_IN_PT = int(A4_HEIGHT_IN_MM / 25.4 * 72)


class PaperTooLargeException(BaseException):
    pass


class PageSet:
    margin = 10*mm

    def __init__(self, document, papers):
        self.document = document
        self.papers = papers

        self.paper_width = papers[0].width
        self.paper_height = papers[0].height
        self.page_width = document.width
        self.page_height = document.height

    def add_to_document(self):



        # How many papers fit on the page?
        number_of_papers_portrait = int((self.page_width - 2*self.margin)/self.paper_width) * \
            int((self.page_height - 2*self.margin)/self.paper_height)
        number_of_papers_landscape = int((self.page_height - 2*self.margin)/self.paper_width) * \
            int((self.page_width - 2*self.margin)/self.paper_height)

        if number_of_papers_landscape > number_of_papers_portrait:
            self.orientation = LANDSCAPE
            self.capacity = number_of_papers_landscape
        else:
            self.orientation = PORTRAIT
            self.capacity = number_of_papers_portrait

        if self.capacity == 0:
            raise PaperTooLargeException()

    @property
    def width(self):
        return self.page_width if self.orientation == PORTRAIT else self.page_height

    @property
    def height(self):
        return self.page_height if self.orientation == PORTRAIT else self.page_width

    def add_papers(self, papers):
        if len(papers) > self.capacity:
            raise Exception(f"{len(papers)} papers on a page with room for {self.capacity}")

        # TODO
        # self.context.save()
        # if self.orientation == LANDSCAPE:
        #     self.context.transform(cairo.Matrix(0,-1,1,0,0,self.page_height))

        self.add_register_marks()
        n_papers_per_row = int((self.width - 2*self.margin)/self.paper_width)
        for i, paper in enumerate(papers):
            column = i//n_papers_per_row
            row = i % n_papers_per_row

            self.canvas.draw(paper.canvas, self.margin + row * self.paper_width,
                                            self.margin + column * self.paper_height)
            self.context.set_source_surface(paper.surface, self.margin + row * self.paper_width,
                                            self.margin + column * self.paper_height)
            self.context.paint()

        # self.context.restore()

    def add_register_marks(self):
        x = self.margin
        while x <= self.width - self.margin:
            Draw.line(self.canvas, (x, 0), (x, self.margin-2*mm), LineStyle(Colour.black, 1))
            Draw.line(self.canvas, (x, self.height), (x, self.height - self.margin + 2*mm), LineStyle(Colour.black, 1))
            x += self.paper_width

        y = self.margin
        while y <= self.height - self.margin:
            Draw.line(self.canvas, (0, y), (self.margin - 2*mm, y), LineStyle(Colour.black, 1))
            Draw.line(self.canvas, (self.width, y), (self.width - self.margin + 2*mm, y), LineStyle(Colour.black, 1))
            y += self.paper_height

    @classmethod
    def fits(cls, paper):
        if paper.width < cls.page_width-2*cls.margin and paper.height < cls.page_height-2*cls.margin:
            return True
        if paper.width < cls.page_height-2*cls.margin and paper.height < cls.page_width-2*cls.margin:
             return True
        return False

    @classmethod
    def split_too_large_paper(cls, paper):
        n_horizontal_pages = math.ceil(paper.width/(cls.page_width-2*cls.margin))
        n_vertical_pages = math.ceil(paper.height/(cls.page_height-2*cls.margin))

        width_map_part = paper.width/n_horizontal_pages
        height_map_part = paper.height/n_vertical_pages

        for column in range(n_horizontal_pages):
            for row in range(n_vertical_pages):
                paper_part = Paper.Paper(width_map_part, height_map_part)

                paper_part.canvas.draw(paper.canvas, (-column*width_map_part, -row*height_map_part))
                # paper_part.context.set_source_surface(paper.surface, -column*width_map_part, -row*height_map_part)
                # paper_part.context.paint()
                yield paper_part


class Output:
    def __init__(self, game, margin=10*mm):
        self.game = game
        self.margin = margin
        self.document = None

    def generate(self):
        self.document = Draw.Document("out.ps", A4_WIDTH_IN_PT, A4_HEIGHT_IN_PT, 10*mm)

        papers = []

        for map in self.game.maps:
            papers.append(map.paper())

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
            paper_parts = list(self.document.split_into_parts(paper))
            papers_by_dimension[(paper_parts[0].width, paper_parts[0].height)] += paper_parts

        for paper_list in papers_by_dimension.values():
            self.document.add_papers(paper_list)

        # current_x_left = self.margin
        # current_y_top = self.margin
        # current_line = 0
        # for tile in self.game.tiles:
        #     if current_x_left + tile.width >= A4_WIDTH_IN_PT - self.margin:
        #         current_y_top += tile.height
        #         current_line += 1
        #         current_x_left = self.margin + tile.width * (current_line % 2) / 2
        #         if current_y_top + tile.height >= A4_HEIGHT_IN_PT - self.margin:
        #             self.context.show_page()
        #             current_x_left = self.margin
        #             current_y_top = self.margin
        #             current_line = 0
        #
        #     self.context.set_source_surface(tile.draw(), current_x_left + tile.width/2, current_y_top+tile.height/2)
        #     self.context.paint()
        #     current_x_left += tile.width
        #
        # self.context.show_page()

        # Tokens
        # size = 2*logo_radius + 7*mm
        # number_per_row = PageSet.page_width // size
        #
        # for i, token in enumerate(self.game.tokens):
        #     x = self.margin + (i % number_per_row) * size
        #     y = self.margin + (i // number_per_row) * size
        #     self.context.set_source_surface(token, x, y)
        #     self.context.paint()

        self.document.surface.finish()
        subprocess.run(['ps2pdf', 'out.ps'])


#
# # Run program fc-list to see all fonts
# font_map = PangoCairo.FontMap.get_default()
# fonts = [font.get_name() for font in font_map.list_families()]