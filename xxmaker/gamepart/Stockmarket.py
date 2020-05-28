from . import Paper
from Definitions import mm
import Colour
from graphics.cairo import Draw
from graphics.cairo.Draw import LineStyle, FillStyle, TextStyle
import Font


class Stockmarket:
    margin = 10*mm

    def __init__(self, cells, has_par_box=False):
        self.game = None
        self.has_par_box = has_par_box
        if has_par_box:
            self.parbox = Parbox(stockmarket=self)
        else:
            self.parbox = None

        self.cells = dict()
        for i, row in enumerate(cells):
            for j, val in enumerate(row):
                if val is not None:
                    self.cells[i, j] = Cell(row=i, column=j, value=val, stockmarket=self)

        for cell in self.cells.values():
            if (cell.row, cell.column-1) not in self.cells and \
                    (cell.row+1, cell.column) in self.cells:
                cell.down_arrow = True
            if (cell.row, cell.column+1) not in self.cells and \
                    (cell.row-1, cell.column) in self.cells:
                cell.up_arrow = True

        self.current_round_marker = None
        self.round_surface = None

    @property
    def width(self):
        return max(cell.column for cell in self.cells.values()) + 1

    @property
    def height(self):
        return max(cell.row for cell in self.cells.values()) + 1

    def paper(self):
        paper = Paper.Paper(self.width*Cell.width+2*self.margin, self.height*Cell.height+2*self.margin)
        c = paper.canvas
        for cell in self.cells.values():
            cell.draw(c)

        if self.current_round_marker:
            self.round_surface = self.current_round_marker.draw()
            c.draw(self.round_surface, (paper.width - self.margin - self.round_surface.width,
                                        paper.height - self.margin - self.round_surface.height))

        if self.has_par_box:
            self.parbox.draw(c)

        return paper

    def par_values(self):
        return sorted([cell.value for cell in self.cells.values() if cell.is_par])

    def max_column_in_row(self, row):
        return max(cell.column for cell in self.cells.values() if cell.row == row)

    def max_row_in_column(self, column):
        return max(cell.row for cell in self.cells.values() if cell.column == column)


class Cell:
    width = 19 * mm
    height = 22 * mm

    def __init__(self, row, column, value, stockmarket, colour=None, down_arrow=None, up_arrow=None):
        self.row = row
        self.column = column
        self.value = value
        self.stockmarket = stockmarket
        self.colour = colour
        self.down_arrow = down_arrow
        self.up_arrow = up_arrow
        self.is_par = False
        self.text = None

    @property
    def x(self):
        return self.column * self.width + Stockmarket.margin

    @property
    def y(self):
        return self.row * self.height + Stockmarket.margin

    def draw(self, c):
        if self.colour:
            Draw.rectangle(c, (self.x, self.y), self.width, self.height,
                           FillStyle(self.colour), LineStyle(Colour.black, 1))
        elif self.is_par:
            Draw.rectangle(c, (self.x, self.y), self.width, self.height,
                           FillStyle(Colour.par), LineStyle(Colour.black, 1))
        else:
            Draw.rectangle(c, (self.x, self.y), self.width, self.height,
                           LineStyle(Colour.black, 1))

        if self.is_par and not self.colour:
            Draw.rectangle(c, (self.x + 2*mm, self.y + 2*mm), self.width - 4*mm, self.height - 4*mm,
                           FillStyle(Colour.white))

        text_colour = self.colour.contrast_colour if self.colour else Colour.black
        Draw.text(c, (self.x+2*mm, self.y+1*mm), self.value, TextStyle(Font.Font(size=10), text_colour))

        if self.text:
            Draw.text(c, (self.x + self.width - 1*mm, self.y + self.height - 1*mm), self.text,
                      TextStyle(Font.normal.made_to_fit(self.text, c, self.width-2*mm), text_colour, 'bottom', 'right'))

        if self.down_arrow:
            x, y = self.x+2*mm, self.y + self.height - 1*mm
            points = [[x, y],
                      [x-1*mm, y-6*mm],
                      [x, y-4.5*mm],
                      [x+1*mm, y-6*mm]]
            Draw.polygon(c, points, FillStyle(Colour.black))
        if self.up_arrow:
            x, y = self.x + self.width-2*mm, self.y+1*mm
            points = [[x, y],
                      [x-1*mm, y+6*mm],
                      [x, y+4.5*mm],
                      [x+1*mm, y+6*mm]]
            Draw.polygon(c, points, FillStyle(Colour.black))

        companies = [company.abbreviation for company in self.stockmarket.game.companies.values()
                     if company.par_price == self.value]
        y = self.y + self.height-1*mm
        for company in sorted(companies, reverse=True):
            Draw.text(c, (self.x+self.width-1*mm, y), company, TextStyle(Font.very_small, Colour.black, 'bottom', 'right'))
            y -= 3*mm


class Parbox:
    margin = 8*mm

    def __init__(self, stockmarket):
        self.stockmarket = stockmarket

    def draw(self, canvas):
        left, top = self.location_topleft()
        right, bottom = self.location_bottomright(canvas)

        width = right - left
        par_values = self.stockmarket.par_values()
        cell_width = width / len(par_values)

        if cell_width > 1.5 * Cell.width:
            cell_width = 1.5 * Cell.width
            width = len(par_values) * cell_width

        height = bottom - top
        Draw.rectangle(canvas, (left, top), width, height, LineStyle(Colour.black, 1), FillStyle(Colour.par))

        for i, par in enumerate(par_values):
            x = left + i * cell_width
            Draw.rectangle(canvas, (x, top), cell_width, height, LineStyle(Colour.black, 1))
            Draw.text(canvas, (x+3*mm, top+1*mm), par, TextStyle(Font.Font(size=12), Colour.black))

        # Draw.text(canvas, (right, top), 'Par values', TextStyle(Font.small, Colour.black, 'bottom', 'right'))

    def location_topleft(self):
        # Determine how much room there is in the last two rows
        row = self.stockmarket.height - 2
        column = self.stockmarket.max_column_in_row(row) + 1

        cell = Cell(row, column, None, self.stockmarket)
        x = cell.x + self.margin
        y = cell.y + self.margin
        return x, y

    def location_bottomright(self, canvas):
        x = canvas.width - self.stockmarket.margin
        y = canvas.height - self.stockmarket.margin

        if self.stockmarket.current_round_marker:
            x -= self.stockmarket.round_surface.width + self.margin

        return x, y
