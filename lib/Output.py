import cairo
import Paper
import collections
from gi.repository import Pango, PangoCairo
import math
from Definitions import *
import subprocess


A4_WIDTH_IN_MM = 210
A4_HEIGHT_IN_MM = 297

A4_WIDTH_IN_PT = int(A4_WIDTH_IN_MM / 25.4 * 72)
A4_HEIGHT_IN_PT = int(A4_HEIGHT_IN_MM / 25.4 * 72)


class PaperTooLargeException(BaseException):
    pass


class Page:
    page_width = 210*mm
    page_height = 297*mm
    margin = 10*mm

    def __init__(self, context, paper_width=None, paper_height=None):
        self.context = context
        self.paper_width = paper_width
        self.paper_height = paper_height

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

        self.context.save()
        if self.orientation == LANDSCAPE:
            self.context.transform(cairo.Matrix(0,-1,1,0,0,self.page_height))

        self.add_register_marks()
        n_papers_per_row = int((self.width - 2*self.margin)/self.paper_width)
        for i, paper in enumerate(papers):
            column = i//n_papers_per_row
            row = i % n_papers_per_row

            self.context.set_source_surface(paper.surface, self.margin + row * self.paper_width,
                                            self.margin + column * self.paper_height)
            self.context.paint()

        self.context.restore()

    def add_register_marks(self):
        self.context.set_source_rgb(0, 0, 0)
        self.context.set_line_width(1)

        x = self.margin
        while x <= self.width - self.margin:
            self.context.move_to(x, 0)
            self.context.line_to(x, self.margin - 2*mm)
            self.context.move_to(x, self.height)
            self.context.line_to(x, self.height - self.margin + 2*mm)
            x += self.paper_width

        y = self.margin
        while y <= self.height - self.margin:
            self.context.move_to(0, y)
            self.context.line_to(self.margin - 2*mm, y)
            self.context.move_to(self.width, y)
            self.context.line_to(self.width - self.margin + 2*mm, y)
            y += self.paper_height

        self.context.stroke()

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

                paper_part.context.set_source_surface(paper.surface, -column*width_map_part, -row*height_map_part)
                paper_part.context.paint()
                yield paper_part


class Output:
    def __init__(self, game, margin=10*mm):
        self.game = game
        self.margin = margin
        self.context = None
        self.surface = None

    def generate(self):
        self.create_pdf_surface()

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
            if Page.fits(paper):
                papers_by_dimension[(paper.width, paper.height)].append(paper)
            else:
                paper_parts = list(Page.split_too_large_paper(paper))
                papers_by_dimension[(paper_parts[0].width, paper_parts[0].height)] += paper_parts

        for (width, height), paper_list in papers_by_dimension.items():
            while paper_list:
                page = Page(self.context, width, height)
                papers_on_this_page = paper_list[:page.capacity]
                paper_list = paper_list[page.capacity:]

                page.add_papers(papers_on_this_page)
                self.context.show_page()

        current_x_left = self.margin
        current_y_top = self.margin
        current_line = 0
        for tile in self.game.tiles:
            if current_x_left + tile.width >= A4_WIDTH_IN_PT - self.margin:
                current_y_top += tile.height
                current_line += 1
                current_x_left = self.margin + tile.width * (current_line % 2) / 2
                if current_y_top + tile.height >= A4_HEIGHT_IN_PT - self.margin:
                    self.context.show_page()
                    current_x_left = self.margin
                    current_y_top = self.margin
                    current_line = 0

            self.context.set_source_surface(tile.draw(), current_x_left + tile.width/2, current_y_top+tile.height/2)
            self.context.paint()
            current_x_left += tile.width

        self.context.show_page()

        # Tokens
        if self.game.stockmarket and self.game.stockmarket.has_par_box:
            tokens_per_company = 3      # stock vale; revenue chart; par value
        else:
            tokens_per_company = 2      # stock value; revenue chart

        tokens = []
        for company in self.game.companies.values():
            tokens += [company.logo] * (company.n_stations + tokens_per_company)

        size = 2*logo_radius + 7*mm
        number_per_row = Page.page_width // size

        for i, token in enumerate(tokens):
            x = self.margin + (i % number_per_row) * size
            y = self.margin + (i // number_per_row) * size
            self.context.set_source_surface(token, x, y)
            self.context.paint()

        self.surface.finish()
        subprocess.run(['ps2pdf', 'out.ps'])

    def create_pdf_surface(self):
        self.surface = cairo.PSSurface("out.ps", A4_WIDTH_IN_PT, A4_HEIGHT_IN_PT)
        self.context = cairo.Context(self.surface)

#
# # Run program fc-list to see all fonts
# font_map = PangoCairo.FontMap.get_default()
# fonts = [font.get_name() for font in font_map.list_families()]