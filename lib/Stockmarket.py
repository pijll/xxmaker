import Paper
from Definitions import mm
import Colour
import OutputFunctions
import Draw
from Draw import LineStyle, FillStyle, TextStyle
import Font


class Stockmarket:
    margin = 10*mm

    def __init__(self, cells, has_par_box=False):
        self.has_par_box = has_par_box

        self.cells = dict()
        for i, row in enumerate(cells):
            for j, val in enumerate(row):
                self.cells[i, j] = Cell(row=i, column=j, value=val)

        for cell in self.cells.values():
            if (cell.row, cell.column-1) not in self.cells and \
                    (cell.row+1, cell.column) in self.cells:
                cell.down_arrow = True
            if (cell.row, cell.column+1) not in self.cells and \
                    (cell.row-1, cell.column) in self.cells:
                cell.up_arrow = True

        self.current_round_marker = None

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
            round_surface = self.current_round_marker.draw()
            c.draw(round_surface, (paper.width - self.margin - round_surface.width,
                                   paper.height - self.margin - round_surface.height))

        return paper


class Cell:
    width = 15 * mm
    height = 16 * mm

    def __init__(self, row, column, value, colour=None, down_arrow=None, up_arrow=None):
        self.row = row
        self.column = column
        self.value = value
        self.colour = colour
        self.down_arrow = down_arrow
        self.up_arrow = up_arrow
        self.is_par = False

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
                           FillStyle(Colour.lightgreen), LineStyle(Colour.black, 1))
        else:
            Draw.rectangle(c, (self.x, self.y), self.width, self.height,
                           LineStyle(Colour.black, 1))

        if self.is_par and not self.colour:
            Draw.rectangle(c, (self.x + 2*mm, self.y + 2*mm), self.width - 4*mm, self.height - 4*mm,
                           FillStyle(Colour.white))

        text_colour = self.colour.contrast_colour if self.colour else Colour.black
        Draw.text(c, (self.x+1*mm, self.y+1*mm), self.value, TextStyle(Font.normal, text_colour))

        if self.down_arrow:
            x, y = self.x+2*mm, self.y + self.height - 1*mm
            points = [[x, y],
                      [x-1*mm, y-6*mm],
                      [x, y-4.5*mm],
                      [x+1*mm, y-6*mm]]
            Draw.polygon(c, points, FillStyle(Colour.black))
            # c.move_to(self.x + 2*mm, self.y + self.height - 1*mm)
            # c.rel_line_to(-1*mm, -6*mm)
            # c.rel_line_to(1*mm, 1.5*mm)
            # c.rel_line_to(1*mm, -1.5*mm)
            # c.close_path()
            # c.fill()
        if self.up_arrow:
            x, y = self.x + self.width-2*mm, self.y+1*mm
            points = [[x, y],
                      [x-1*mm, y+6*mm],
                      [x, y+4.5*mm],
                      [x+1*mm, y+6*mm]]
            Draw.polygon(c, points, FillStyle(Colour.black))
            # c.move_to(self.x + self.width - 2*mm, self.y + 1*mm)
            # c.rel_line_to(-1*mm, 6*mm)
            # c.rel_line_to(1*mm, -1.5*mm)
            # c.rel_line_to(1*mm, 1.5*mm)
            # c.close_path()
            # c.fill()
