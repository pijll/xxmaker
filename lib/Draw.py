import tempfile

import cairo
from gi.repository import Pango, PangoCairo
from Definitions import *
import subprocess
import Colour
import os
import Font


end_cap_round = object()


class Canvas:
    def __init__(self, corner, width, height, surface=None, context=None):
        """Create a new drawing surface.

        corner: the coordinates of the top left corner of the canvas."""
        self.corner = corner
        self.width = width
        self.height = height

        self.surface = surface or cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(*corner, width, height))
        self.context = context or cairo.Context(self.surface)

        self.license_info = {}

    def draw(self, canvas, location, black_and_white=False, alpha=None, rotated=False):
        """Paint one canvas on the other, at location x,y = location."""
        # Copy license info to this canvas
        self.license_info.update(canvas.license_info)

        if rotated:
            source_canvas = Canvas((0, 0), canvas.height, canvas.width)
            source_canvas.context.translate(canvas.height, 0)
            source_canvas.context.rotate(3.14159 / 2)
            source_canvas.context.set_source_surface(canvas.surface)
            source_canvas.context.paint()
        else:
            source_canvas = canvas

        self.context.set_source_surface(source_canvas.surface, *location)
        if alpha is None:
            self.context.paint()
        else:
            self.context.paint_with_alpha(alpha)

        if black_and_white:
            self.context.set_source_rgba(1, 1, 1)
            self.context.set_operator(cairo.OPERATOR_HSL_COLOR)
            self.context.rectangle(*location, source_canvas.width, source_canvas.height)
            self.context.fill()


class Page(Canvas):
    def __init__(self, document):
        super().__init__((0, 0), document.width, document.height, document.surface, document.context)
        self.license_info = document.license_info

    def add_register_marks(self, paper_width, paper_height, margin):
        x = margin
        while x <= self.width - margin:
            line(self, (x, 0), (x, margin - 2 * mm), LineStyle(Colour.black, 1))
            line(self, (x, self.height), (x, self.height - margin + 2 * mm), LineStyle(Colour.black, 1))
            x += paper_width

        y = margin
        while y <= self.height - margin:
            line(self, (0, y), (margin - 2 * mm, y), LineStyle(Colour.black, 1))
            line(self, (self.width, y), (self.width - margin + 2 * mm, y), LineStyle(Colour.black, 1))
            y += paper_height


class Document:
    def __init__(self, filename, width, height, margin):
        self.filename = filename
        self.width = width
        self.height = height
        self.margin = margin

        self.surface = cairo.PSSurface(filename, width, height)
        self.context = cairo.Context(self.surface)
        self.number_of_pages = 0
        self.license_info = {}

    def new_page(self):
        if self.number_of_pages > 0:
            self.context.show_page()
        self.number_of_pages += 1
        return Page(self)

    def add_papers(self, paper_list):
        """Add papers to the document.

        Every paper has to have the same size (width x height)."""
        def how_many_fit_on_page(page_size, paper_size):
            return int((page_size - 2*self.margin) / (paper_size))

        w, h = paper_list[0].width, paper_list[0].height

        capacity_portrait = how_many_fit_on_page(self.width, w) * how_many_fit_on_page(self.height, h)
        capacity_landscape = how_many_fit_on_page(self.height, w) * how_many_fit_on_page(self.width, h)

        papers_are_rotated = (capacity_landscape > capacity_portrait)

        if papers_are_rotated:
            w, h = h, w
        n_papers_per_row = how_many_fit_on_page(self.width, w)
        n_papers_per_column = how_many_fit_on_page(self.height, h)

        page = None
        for i, paper in enumerate( paper_list):
            column = i % n_papers_per_row
            row = (i//n_papers_per_row) % n_papers_per_column

            if row == 0 and column == 0:
                page = self.new_page()
                page.add_register_marks(w, h, self.margin)

            page.draw(paper.canvas, (self.margin + column * w, self.margin + row * h), rotated=papers_are_rotated)

    def finish(self):
        self.surface.finish()
        subprocess.run(['ps2pdf', self.filename])


class LineStyle:
    def __init__(self, colour, width, dashed=False, end_cap=None):
        self.colour = colour
        self.width = width
        self.dashed = dashed
        self.end_cap = end_cap


class FillStyle:
    def __init__(self, colour):
        self.colour = colour


def _draw(canvas, styles):
    context = canvas.context

    for i, style in enumerate(styles):
        laatste_argument = (i == len(styles) - 1)
        if isinstance(style, FillStyle):
            context.set_source_rgb(*style.colour.rgb)
            if laatste_argument:
                context.fill()
            else:
                context.fill_preserve()
        elif isinstance(style, LineStyle):
            context.set_source_rgb(*style.colour.rgb)
            context.set_line_width(style.width)
            if style.dashed or style.end_cap:
                context.save()
                context_saved = True
            else:
                context_saved = False
            if style.dashed:
                context.save()
                context.set_dash([1*mm])
            if style.end_cap == end_cap_round:
                context.set_line_cap(cairo.LineCap.ROUND)
            if laatste_argument:
                context.stroke()
            else:
                context.stroke_preserve()
            if context_saved:
               context.restore()


def line(canvas, start, end, *line_styles):
    """Drows a line between two points."""
    canvas.context.move_to(*start)
    canvas.context.line_to(*end)
    _draw(canvas, line_styles)


def polygon(canvas, points, *styles):
    canvas.context.move_to(*points[-1])
    for point in points:
        canvas.context.line_to(*point)
    canvas.context.close_path()

    _draw(canvas, styles)


def circle(canvas, center, radius, *styles):
    canvas.context.arc(*center, radius, 0, 2*3.142)
    _draw(canvas, styles)


def arc(canvas, center, radius, angle_start, angle_end, *styles):
    canvas.context.arc(*center, radius, angle_start, angle_end)
    _draw(canvas, styles)


def triangle(canvas, center, side_length, *styles):
    """Draw an upright equilateral triangle."""
    height = 3**.5 / 2 * side_length
    points = [(center[0] + x, center[1] + y)
              for x,y in [(0, -height*2/3), (+side_length/2, height/3), (-side_length/2, height/3)]]
    polygon(canvas, points, *styles)


def rectangle(canvas, corner, width, height, *styles):
    x, y = corner
    points = [(x, y), (x+width, y), (x+width, y+height), (x, y+height)]
    polygon(canvas, points, *styles)


class TextStyle:
    def __init__(self, font, colour, valign='top', halign='left'):
        self.colour = colour
        self.font = font
        self.valign = valign
        self.halign = halign


def text(canvas, location, txt, textstyle):
    context = canvas.context
    layout = PangoCairo.create_layout(context)
    layout.set_font_description(textstyle.font.description)
    layout.set_text(str(txt))

    ink_extent, extent_text = layout.get_extents()
    text_width, text_height = extent_text.width / Pango.SCALE, extent_text.height / Pango.SCALE
    ink_top_edge = ink_extent.y / Pango.SCALE
    ink_height = ink_extent.height / Pango.SCALE

    x, y = location
    if textstyle.valign == 'top':
        y_reference = y
    elif textstyle.valign == 'bottom':
        y_reference = y - text_height
    elif textstyle.valign == 'centre' or textstyle.valign == 'center':
        y_reference = y - text_height / 2
    elif textstyle.valign == 'exactcentre' or textstyle.valign == 'exactcenter':
        y_reference = y - ink_top_edge - ink_height / 2
    else:
        assert False

    if textstyle.halign == 'left':
        x_reference = x
    elif textstyle.halign == 'right':
        x_reference = x - text_width
    elif textstyle.halign == 'centre' or textstyle.halign == 'center':
        x_reference = x - text_width / 2
    elif textstyle.halign == 'exactcentre' or textstyle.halign == 'exactcenter':
        x_reference = x - ink_extent.width / 2 / Pango.SCALE
    else:
        assert False

    context.set_source_rgb(*textstyle.colour.rgb)
    context.move_to(x_reference, y_reference)
    PangoCairo.show_layout(context, layout)
    context.stroke()


def load_image(canvas, filename, center, width, height, circle_clip=False):
    """Filename should be relative to the graphics directory."""
    home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    complete_filename = os.path.join(home_dir, 'graphics', filename)

    license_file = complete_filename + '.txt'
    try:
        with open(license_file) as infile:
            license_txt = infile.read()
    except OSError:
        raise Exception(f"No license file found for file '{filename}'") from None

    canvas.license_info[filename] = license_txt

    if complete_filename.endswith('.svg'):
        complete_filename = convert_svg_to_png(complete_filename)
    try:
        image = cairo.ImageSurface.create_from_png(complete_filename)
    except cairo.Error:
        print(f'{cairo.Error}, filename={filename}')
        return False

    img_width = image.get_width()
    img_height = image.get_height()

    scale = min(width / image.get_width(), height / image.get_height())

    context = canvas.context
    context.save()
    context.scale(scale, scale)
    context.set_source_surface(image, center[0]/scale - img_width/2, center[1]/scale - img_height/2)
    if circle_clip:
        context.arc(center[0]/scale, center[1]/scale, max(img_width, img_height)/2, 0, 6.29)
        context.clip()
    context.paint()
    context.restore()
    return True


def convert_svg_to_png(complete_filename):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    filename_png = temp_file.name
    temp_file.close()
    subprocess.run(['convert', complete_filename, '-transparent', 'white', filename_png])
    return filename_png
