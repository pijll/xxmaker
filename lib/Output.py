import cairo
import Paper
import collections
from gi.repository import Pango, PangoCairo
import math


A4_WIDTH_IN_MM = 210
A4_HEIGHT_IN_MM = 297

A4_WIDTH_IN_PT = int(A4_WIDTH_IN_MM / 25.4 * 72)
A4_HEIGHT_IN_PT = int(A4_HEIGHT_IN_MM / 25.4 * 72)


inch = 72
mm = inch/25.4

LANDSCAPE = 1
PORTRAIT = 2


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

        papers.append(Paper.priority_deal())

        papers_by_dimension = collections.defaultdict(list)
        for paper in papers:
            if Page.fits(paper):
                papers_by_dimension[(paper.width, paper.height)].append(paper)
            else:
                paper_parts = list(Page.split_too_large_paper(paper))
                print(len(paper_parts))
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

        self.surface.finish()

    def create_pdf_surface(self):
        self.surface = cairo.PDFSurface("out.pdf", A4_WIDTH_IN_PT, A4_HEIGHT_IN_PT)
        self.context = cairo.Context(self.surface)


def load_image(filename, context, x_c, y_c, width, height):
    try:
        image = cairo.ImageSurface.create_from_png(filename)
    except cairo.Error:
        print(f'{cairo.Error}, filename={filename}')
        return

    img_width = image.get_width()
    img_height = image.get_height()

    scale = min(width / image.get_width(), height / image.get_height())

    context.save()
    context.scale(scale, scale)
    context.set_source_surface(image, x_c/scale - img_width/2, y_c/scale - img_height/2)
    context.paint()
    context.restore()


def move_to_text(context, text, x, y, valign='top', halign='left'):
    # The vertical alignment is determined by the font, not the specific text.
    # This means that a text with "tall letters" and one without them get aligned equally.
    if valign == 'top':
        font_ascent = context.font_extents()[0]
        y_reference = y + font_ascent
    elif valign == 'bottom':
        font_descent = context.font_extents()[1]
        y_reference = y - font_descent
    elif valign == 'centre' or valign == 'center':
        font_ascent, font_descent, *_ = context.font_extents()
        y_reference = y + font_ascent/2 - font_descent/2
    else:
        assert False

    if halign == 'left':
        x_reference = x
    elif halign == 'right':
        x_advance = context.text_extents(text)[4]
        x_reference = x - x_advance
    elif halign == 'centre' or halign == 'center':
        x_advance = context.text_extents(text)[4]
        x_reference = x - x_advance/2
    else:
        assert False

    context.move_to(x_reference, y_reference)


# Run program fc-list to see all fonts
font_map = PangoCairo.FontMap.get_default()
fonts = [font.get_name() for font in font_map.list_families()]


def draw_text(text, font_name, font_size, context, x, y, valign='top', halign='left'):
    layout = PangoCairo.create_layout(context)
    font = Pango.FontDescription(f"{font_name} {font_size}")
    layout.set_font_description(font)
    layout.set_text(text)

    extent_text = layout.get_extents()[1]
    text_width, text_height = extent_text.width / Pango.SCALE, extent_text.height / Pango.SCALE

    if valign == 'top':
        y_reference = y
    elif valign == 'bottom':
        y_reference = y - text_height
    elif valign == 'centre' or valign == 'center':
        y_reference = y - text_height / 2
    else:
        assert False

    if halign == 'left':
        x_reference = x
    elif halign == 'right':
        x_reference = x - text_width
    elif halign == 'centre' or halign == 'center':
        x_reference = x - text_width / 2
    else:
        assert False

    context.move_to(x_reference, y_reference)
    PangoCairo.show_layout(context, layout)


def draw_centered_lines(text, font_name, font_size, context, x_c, y, width, valign='center'):
    layout = PangoCairo.create_layout(context)
    font = Pango.FontDescription(f"{font_name} {font_size}")
    layout.set_font_description(font)
    layout.set_width(width*Pango.SCALE)
    layout.set_alignment(Pango.Alignment.CENTER)
    layout.set_wrap(Pango.WrapMode.WORD_CHAR)
    layout.set_text(text)
    extent_text = layout.get_extents()[1]

    if valign == 'top':
        y_reference = y
    elif valign == 'bottom':
        y_reference = y - extent_text.height / Pango.SCALE
    elif valign == 'centre' or valign == 'center':
        y_reference = y - extent_text.height / Pango.SCALE / 2
    else:
        assert False

    context.set_source_rgb(0, 0, 0)
    x, y = x_c - width / 2, y_reference
    context.move_to(x, y)
    PangoCairo.show_layout(context, layout)
